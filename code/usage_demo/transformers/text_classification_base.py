#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-06-10 11:31 上午
    
Author:
    huayang
    
Subject:
    文本分类
"""

import os
import math
import random
import logging

from typing import *

import datasets
import transformers
import torch.nn as nn

from tqdm.auto import tqdm
from datasets import load_dataset, load_metric
from accelerate import Accelerator

from torch.utils.data.dataloader import DataLoader

from transformers import set_seed
from transformers.optimization import AdamW, get_scheduler
from transformers.data.data_collator import default_data_collator
from transformers.models.auto import AutoModelForSequenceClassification, AutoTokenizer, AutoConfig

from my_utils.config import BaseConfig

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class Config(BaseConfig):
    def __init__(self, **kwargs):
        """"""
        # 任务相关
        self.file_type = 'json'  # 推荐使用 json 格式，csv 需要指定处理一些特殊符号，text 需要自己写 map
        # json 格式一行一条数据，不是标准的 json 文件，如：
        #   {"seq": "my_text_1_sentence_1", "label": 1}
        #   {"seq": "my_text_1_sentence_2", "label": 0}

        self.train_file: Union[str, List[str]] = ''
        self.val_file: Union[str, List[str]] = ''
        self.test_file: Union[str, List[str]] = ''
        self.label_column_name = 'label'  # label 列的名称，如果存在
        self.num_labels: int = 2
        self.max_length: int = 128

        # 常用超参
        self.batch_size: int = 32
        self.weight_decay: float = 0.01
        self.learning_rate: float = 1.e-5
        self.num_train_epochs: int = 3
        self.max_train_steps = None  # 与 num_train_epochs 二选一
        self.num_warmup_steps: int = 0
        self.gradient_accumulation_steps: int = 2  # 梯度累计，模拟更大的 batch_size

        # base 模型
        self.base_model_id = 'hfl/chinese-roberta-wwm-ext'
        # 模型模型索引：https://huggingface.co/models?filter=bert
        # 常用中文模型：
        #   'bert-base-chinese'
        #   'hfl/chinese-bert-wwm'
        #   'hfl/chinese-bert-wwm-ext'
        #   'hfl/chinese-roberta-wwm-ext'
        #   'hfl/chinese-roberta-wwm-ext-large'
        #   'hfl/chinese-macbert-base'
        #   'hfl/chinese-macbert-large'

        self.no_decay = ["bias", "LayerNorm.weight"]
        self.output_dir = './out_model'
        self.metric = 'accuracy'
        self.lr_scheduler_type = 'linear'
        self.random_seed = None
        self.pad_to_max_length = True
        self.num_train_data = None

        super(Config, self).__init__(**kwargs)


def set_random_seed(args: Config):
    """"""
    if args.random_seed is not None:
        assert isinstance(args.random_seed, int), '`args.random_seed` should be int.'
        set_seed(args.random_seed)


def main(args: Config):
    """"""
    accelerator = Accelerator()
    logger.info(f'accelerator state:\n{accelerator.state}')

    # 设置随机数
    set_random_seed(args)

    # 模型准备
    logger.info('***** Model prepare *****')
    model, tokenizer = model_prepare(args)

    # 数据准备
    logger.info('***** Data prepare *****')
    train_dl, val_dl = data_prepare(args, tokenizer)

    # 优化器准备
    logger.info('***** Optimizer prepare *****')
    optimizer = optimizer_prepare(args, model)

    # accelerator prepare
    model, optimizer, train_dl, val_dl = accelerator.prepare(model, optimizer, train_dl, val_dl)

    # prepare lr_scheduler
    num_update_steps_per_epoch = math.ceil(len(train_dl) / args.gradient_accumulation_steps)
    args.max_train_steps = args.num_train_epochs * num_update_steps_per_epoch
    lr_scheduler = get_scheduler(name=args.lr_scheduler_type,
                                 optimizer=optimizer,
                                 num_warmup_steps=args.num_warmup_steps,
                                 num_training_steps=args.max_train_steps, )

    # train
    logger.info("***** Start training *****")
    train(args, model, optimizer, train_dl, val_dl, accelerator, lr_scheduler)

    # 模型保存
    logger.info("***** Model save *****")
    model_save(args, accelerator, model)


def data_prepare(args: Config, tokenizer):
    """"""
    dss = load_dataset(args.file_type,
                       data_files={'train': args.train_file,
                                   'validation': args.val_file})

    # 计算 num_labels
    label_list = sorted(dss["train"].unique("label"))
    num_labels = len(label_list)
    assert args.num_labels == num_labels, 'args.num_labels != num_labels'

    label_to_id = {v: i for i, v in enumerate(label_list)}

    # 判断是单句分类，还是句间关系
    non_label_column_names = [name for name in dss["train"].column_names if name != args.label_column_name]
    if len(non_label_column_names) >= 2:
        sentence1_key, sentence2_key = non_label_column_names[:2]
    else:
        sentence1_key, sentence2_key = non_label_column_names[0], None

    padding = "max_length" if args.pad_to_max_length else False

    def row_precess(row):
        # tokenize the seq
        texts = ((row[sentence1_key],) if sentence2_key is None
                 else (row[sentence1_key], row[sentence2_key]))
        result = tokenizer(*texts, padding=padding, max_length=args.max_length, truncation=True)

        if args.label_column_name in row:
            result['label'] = [label_to_id[it] for it in row[args.label_column_name]]

        return result

    dss = dss.map(row_precess, batched=True, remove_columns=dss["train"].column_names)  # 把原来的列移除
    train_ds, eval_ds = dss['train'], dss['validation']

    # 打印样例数据
    # for index in random.sample(range(len(train_ds)), 3):
    #     logger.info(f"Sample {index} of the training set: {train_ds[index]}.")

    args.num_train_data = len(train_ds)
    train_dl = DataLoader(train_ds, shuffle=True, collate_fn=default_data_collator, batch_size=args.batch_size)
    val_dl = DataLoader(eval_ds, collate_fn=default_data_collator, batch_size=args.batch_size)

    return train_dl, val_dl


def optimizer_prepare(args: Config, model):
    """"""

    def do_weight_decay(n):
        return all(r not in n for r in args.no_decay)

    # named_parameters = list(model.named_parameters())
    params_do_weight_decay, params_no_weight_decay = [], []
    for param_name, param in model.named_parameters():
        if do_weight_decay(param_name):
            params_do_weight_decay.append(param)
        else:
            params_no_weight_decay.append(param)

    optimizer_grouped_parameters = [{"params": params_do_weight_decay, "weight_decay": args.weight_decay},
                                    {"params": params_no_weight_decay, "weight_decay": 0.0}]
    optimizer = AdamW(optimizer_grouped_parameters, lr=args.learning_rate)
    return optimizer


def train(args: Config, model, optimizer, train_dl, val_dl, accelerator, lr_scheduler):
    # metric
    metric = load_metric(args.metric)

    # train
    total_batch_size = args.batch_size * accelerator.num_processes * args.gradient_accumulation_steps
    logger.info("***** Running training *****")
    logger.info(f"  Total batch size = {total_batch_size}")
    logger.info(f"  Num examples = {args.num_train_data}")
    logger.info(f"  Num epochs = {args.num_train_epochs}")
    logger.info(f"  Gradient accumulation steps = {args.gradient_accumulation_steps}")
    logger.info(f"  Total optimization steps = {args.max_train_steps}")

    completed_steps = 0
    progress_bar = tqdm(range(args.max_train_steps), disable=not accelerator.is_local_main_process)
    for epoch in range(args.num_train_epochs):
        model.train()
        for step, batch in enumerate(train_dl):
            outputs = model(**batch)
            loss = outputs.loss / args.gradient_accumulation_steps
            accelerator.backward(loss)

            # 梯度累计，模拟更大的 batch_size
            if step % args.gradient_accumulation_steps == 0 or step == len(train_dl) - 1:
                optimizer.step()
                lr_scheduler.step()
                optimizer.zero_grad()

                completed_steps += 1
                progress_bar.update(1)

            if completed_steps >= args.max_train_steps:
                break

        model.eval()
        for step, batch in enumerate(val_dl):
            outputs = model(**batch)
            predictions = outputs.logits.argmax(dim=-1)
            metric.add_batch(predictions=accelerator.gather(predictions),
                             references=accelerator.gather(batch["labels"]))

        eval_metric = metric.compute()
        logger.info(f"epoch {epoch}: {eval_metric}")


def model_save(args: Config, accelerator, model):
    accelerator.wait_for_everyone()
    model = accelerator.unwrap_model(model)
    model.save_pretrained(args.output_dir, save_function=accelerator.save)


def model_prepare(args: Config):
    config = AutoConfig.from_pretrained(args.base_model_id, num_labels=args.num_labels)
    model = AutoModelForSequenceClassification.from_pretrained(args.base_model_id, config=config)
    tokenizer = AutoTokenizer.from_pretrained(args.base_model_id)
    return model, tokenizer


def run_predict(args: Config):
    """"""
    from transformers import pipeline, TextClassificationPipeline
    model = AutoModelForSequenceClassification.from_pretrained(args.output_dir, num_labels=args.num_labels)
    tokenizer = AutoTokenizer.from_pretrained(args.base_model_id)
    # classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)
    classifier = TextClassificationPipeline(model=model, tokenizer=tokenizer, return_all_scores=True)
    ret = classifier('my_test_sentence_1')
    print(ret)


if __name__ == '__main__':
    """"""
    cfg = Config(train_file=['./data/my_text_1.json', './data/my_text_2.json'],
                 val_file='./data/my_test_file.json')

    main(cfg)
    run_predict(cfg)
