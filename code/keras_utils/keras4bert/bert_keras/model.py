#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-01-23 19:42
    
Author:
    huayang
    
Subject:
    Bert 模型主要代码
    - 模型没有写成类的形式，虽然通过类可以方便的传输内部变量来减少代码量（主要是参数的传递），并拓展模型：
        - 模型拓展可以参考 bojone/bert4keras/models.py 中 UniLM_Mask 的实现及使用，通过继承该类，使 bert 具有直接训练 seq2seq 的能力；
        - 相关文章：从语言模型到Seq2Seq：Transformer如戏，全靠Mask | https://kexue.fm/archives/6933
    - 但也正因为这一点可能会使 tensor 的流向变得不够清晰，这与学习目的相悖。
"""
import json

import numpy as np
import tensorflow as tf

try:
    import tensorflow.keras as keras
    import tensorflow.keras.backend as K
except:
    import keras
    import keras.backend as K

from .layers import *
from .utils import gelu


class _OutputType:
    """模型输出的类型"""
    SENTENCE_EMBEDDING = 'sentence_embedding'
    CLS_EMBEDDING = 'cls_embedding'
    MLM_PROBABILITY = 'mlm_probability'
    NSP_PROBABILITY = 'nsp_probability'

    @staticmethod
    def get_type_set():
        """"""
        return {v for k, v in _OutputType.__dict__.items() if not k.startswith('__') and isinstance(v, str)}


class _LayerName:
    """各层的命名，用于加载 ckpt 时一一对应"""

    def __init__(self, n_transformer_block):
        """"""
        # input layer
        self.input_token = 'Input-Token'
        self.input_segment = 'Input-Segment'
        # embedding layer
        self.embedding_token = 'Embedding-Token'
        self.embedding_segment = 'Embedding-Segment'
        self.embedding_token_segment = 'Embedding-Token-Segment'
        self.embedding_position = 'Embedding-Position'
        self.embedding_norm = 'Embedding-Norm'
        self.embedding_dropout = 'Embedding-Dropout'

        # transform_block
        for block_index in range(n_transformer_block):
            prefix_attr = 'transformer_%s_' % block_index
            prefix_layer = 'Transformer-%s-' % block_index
            setattr(self, prefix_attr + 'attention', prefix_layer + 'MultiHeadSelfAttention')
            setattr(self, prefix_attr + 'attention_dropout', prefix_layer + 'MultiHeadSelfAttention-Dropout')
            setattr(self, prefix_attr + 'attention_add', prefix_layer + 'MultiHeadSelfAttention-Add')
            setattr(self, prefix_attr + 'attention_norm', prefix_layer + 'MultiHeadSelfAttention-Norm')
            setattr(self, prefix_attr + 'feed_forward', prefix_layer + 'FeedForward')
            setattr(self, prefix_attr + 'feed_forward_dropout', prefix_layer + 'FeedForward-Dropout')
            setattr(self, prefix_attr + 'feed_forward_add', prefix_layer + 'FeedForward-Add')
            setattr(self, prefix_attr + 'feed_forward_norm', prefix_layer + 'FeedForward-Norm')

        # output layer
        self.pooler = 'Pooler'
        self.pooler_dense = 'Pooler-Dense'
        self.mlm_dense = 'MLM-Dense'
        self.mlm_norm = 'MLM-Norm'
        self.mlm_softmax = 'MLM-Softmax'
        self.nsp_softmax = 'NSP-Softmax'


def build_bret(config_path=None,
               ckpt_path=None,
               output_type='cls_embedding',
               training=False,
               return_full_model=False,
               return_config=False,
               **kwargs):
    """"""

    def _arg_replace(arg_name, arg_name_new):
        if arg_name in config and arg_name != arg_name_new:
            config[arg_name_new] = config[arg_name]
            config.pop(arg_name)

    def _remove_arg(arg_name):
        config.pop(arg_name)

    def _check_args():
        assert output_type in _OutputType.get_type_set()

    _check_args()
    config = {}
    if config_path is not None:
        config.update(json.load(open(config_path)))

    # 这几个 remove 的参数还没深入研究是怎么用的
    _remove_arg('directionality')
    _remove_arg('pooler_fc_size')
    _remove_arg('pooler_num_attention_heads')
    _remove_arg('pooler_num_fc_layers')
    _remove_arg('pooler_size_per_head')
    _remove_arg('pooler_type')
    _arg_replace('attention_probs_dropout_prob', 'attention_dropout_rate')
    _arg_replace('hidden_act', 'hidden_activation')
    _arg_replace('hidden_dropout_prob', 'dropout_rate')
    _arg_replace('hidden_size', 'n_hidden_unit')
    _arg_replace('initializer_range', 'initializer_range')
    _arg_replace('intermediate_size', 'n_intermediate_unit')
    _arg_replace('max_position_embeddings', 'max_position_len')
    _arg_replace('num_attention_heads', 'n_attention_head')
    _arg_replace('num_hidden_layers', 'n_transformer_block')
    _arg_replace('type_vocab_size', 'segment_vocab_size')
    _arg_replace('vocab_size', 'vocab_size')
    config.update(kwargs)

    model, layer_name = bert(**config, return_layer_name=True)
    load_model_weights_from_checkpoint(model, config, ckpt_path, layer_name)

    # outputs = [sequence_embedding, cls_embedding, mlm_probability, nsp_probability]
    outputs = model.outputs
    if output_type == _OutputType.SENTENCE_EMBEDDING:
        outputs = outputs[0]
    elif output_type == _OutputType.CLS_EMBEDDING:
        outputs = outputs[1]
    elif output_type == _OutputType.MLM_PROBABILITY:
        outputs = outputs[2]
    elif output_type == _OutputType.NSP_PROBABILITY:
        outputs = outputs[3]
    elif training:  # 原始 bert 是一个多任务联合训练模型，包括 MLM 和 NSP，因此有两个输出
        outputs = [outputs[2], outputs[3]]

    model_fix = keras.Model(model.inputs, outputs=outputs, name='Bert_fix')

    ret = [model_fix]
    if return_full_model:
        ret.append(model)

    if return_config:
        ret.append(config)

    return model_fix if len(ret) <= 1 else ret


def bert(n_hidden_unit=768,
         n_transformer_block=12,
         n_attention_head=12,
         n_intermediate_unit=3072,
         vocab_size=21128,
         segment_vocab_size=2,
         max_position_len=512,
         sequence_len=None,
         hidden_activation=gelu,
         n_unit_each_head=None,
         embedding_size=None,
         dropout_rate=0.0,
         attention_dropout_rate=0.0,
         initializer_range=0.02,
         initializer=None,
         return_layer_name=False):
    """"""
    # args assert
    embedding_size = embedding_size or n_hidden_unit
    initializer = initializer or keras.initializers.TruncatedNormal(stddev=initializer_range)

    layer_name = _LayerName(n_transformer_block)

    def _check_args():
        # 目前暂不支持 embedding_size != n_hidden_unit
        assert embedding_size == n_hidden_unit

    _check_args()
    # inputs
    inputs = get_inputs(sequence_len, layer_name)

    # flow
    x, embed_weights = apply_embedding_layer(inputs,
                                             vocab_size,
                                             segment_vocab_size,
                                             max_position_len,
                                             embedding_size,
                                             dropout_rate,
                                             layer_name)

    for block_index in range(n_transformer_block):
        x = apply_transformer_block(x,
                                    block_index,
                                    n_attention_head,
                                    n_unit_each_head,
                                    n_hidden_unit,
                                    attention_dropout_rate,
                                    n_intermediate_unit,
                                    hidden_activation,
                                    initializer,
                                    layer_name)

    outputs = apply_output_layer(x,
                                 embed_weights,
                                 n_hidden_unit,
                                 hidden_activation,
                                 initializer,
                                 layer_name)

    model = keras.Model(inputs, outputs, name='Bert')

    ret = [model]
    if return_layer_name:
        ret.append(layer_name)

    return model if len(ret) <= 1 else ret


def get_inputs(sequence_len, layer_name):
    """"""
    x_in = keras.layers.Input(shape=(sequence_len,), name=layer_name.input_token)
    s_in = keras.layers.Input(shape=(sequence_len,), name=layer_name.input_segment)

    inputs = [x_in, s_in]
    return inputs


def apply_embedding_layer(inputs,
                          vocab_size,
                          segment_vocab_size,
                          max_sequence_len,
                          embedding_size,
                          dropout_rate,
                          layer_name):
    """"""
    inputs = inputs[:]
    x, s = inputs
    # embed_layer = keras.layers.Embedding(input_dim=vocab_size, output_dim=embedding_size, mask_zero=True,
    #                                      name='Embedding-Token')
    # embed_weights = embed_layer.embeddings  # 不能直接获取
    x, embed_weights = CustomEmbedding(input_dim=vocab_size, output_dim=embedding_size, mask_zero=True,
                                       name=layer_name.embedding_token)(x)
    s = keras.layers.Embedding(input_dim=segment_vocab_size, output_dim=embedding_size,
                               name=layer_name.embedding_segment)(s)

    x = CustomAdd(name=layer_name.embedding_token_segment)([x, s])  # [x, s] 的顺序不能变
    x = PositionEmbedding(input_dim=max_sequence_len, output_dim=embedding_size, name=layer_name.embedding_position)(x)
    x = LayerNormalization(name=layer_name.embedding_norm)(x)
    x = keras.layers.Dropout(dropout_rate, name=layer_name.embedding_dropout)(x)

    return x, embed_weights


def apply_transformer_block(inputs,
                            block_index,
                            n_attention_head,
                            n_unit_each_head,
                            n_hidden_unit,
                            dropout_rate,
                            n_intermediate_unit,
                            hidden_act,
                            initializer,
                            layer_name):
    """Att --> Add --> LN --> FFN --> Add --> LN"""
    x = inputs
    xi = x
    x = MultiHeadAttention(n_unit=n_hidden_unit,
                           n_head=n_attention_head,
                           n_unit_each_head=n_unit_each_head,
                           name=getattr(layer_name, 'transformer_%s_attention' % block_index))([x, x, x])
    x = keras.layers.Dropout(dropout_rate,
                             name=getattr(layer_name, 'transformer_%s_attention_dropout' % block_index))(x)
    x = keras.layers.Add(name=getattr(layer_name, 'transformer_%s_attention_add' % block_index))([xi, x])
    x = LayerNormalization(name=getattr(layer_name, 'transformer_%s_attention_norm' % block_index))(x)

    xi = x
    x = FeedForward(units=n_intermediate_unit,
                    activation=hidden_act,
                    kernel_initializer=initializer,
                    name=getattr(layer_name, 'transformer_%s_feed_forward' % block_index))(x)
    x = keras.layers.Dropout(dropout_rate,
                             name=getattr(layer_name, 'transformer_%s_feed_forward_dropout' % block_index))(x)
    x = keras.layers.Add(name=getattr(layer_name, 'transformer_%s_feed_forward_add' % block_index))([xi, x])
    x = LayerNormalization(name=getattr(layer_name, 'transformer_%s_feed_forward_norm' % block_index))(x)

    return x


def apply_output_layer(inputs,
                       embed_weights,
                       n_hidden_unit,
                       hidden_activation,
                       initializer,
                       layer_name):
    """"""
    # 可能包含多个输出
    outputs = []

    x = inputs
    outputs.append(x)  # sentence embedding

    # 提取 [CLS] 向量
    x = outputs[0]  # sentence embedding
    x = keras.layers.Lambda(function=lambda tensor: tensor[:, 0], name=layer_name.pooler)(x)  # 提取 [CLS] embedding
    x = keras.layers.Dense(units=n_hidden_unit, activation='tanh', kernel_initializer=initializer,
                           name=layer_name.pooler_dense)(x)
    outputs.append(x)  # [CLS] 向量

    # Task1: Masked Language
    x = outputs[0]  # sentence embedding
    x = keras.layers.Dense(units=n_hidden_unit, activation=hidden_activation, name=layer_name.mlm_dense)(x)
    x = LayerNormalization(name=layer_name.mlm_norm)(x)
    x = EmbeddingSimilarity(name=layer_name.mlm_softmax)([x, embed_weights])
    outputs.append(x)  # mlm softmax

    # Task2: Next Sentence
    x = outputs[1]  # [CLS] 向量
    x = keras.layers.Dense(units=2, activation='softmax', kernel_initializer=initializer,
                           name=layer_name.nsp_softmax)(x)
    outputs.append(x)  # nsp softmax

    return outputs  # [sequecen embedding, cls embedding, mlm softmax, nsp softmax]


def load_model_weights_from_checkpoint(model,
                                       config,
                                       checkpoint_file,
                                       layer_name: _LayerName):
    """Load trained official model from checkpoint.
    """
    _loader = lambda name: tf.train.load_variable(checkpoint_file, name)

    model.get_layer(name=layer_name.embedding_token).set_weights([
        _loader('bert/embeddings/word_embeddings'),
    ])
    model.get_layer(name=layer_name.embedding_segment).set_weights([
        _loader('bert/embeddings/token_type_embeddings'),
    ])
    model.get_layer(name=layer_name.embedding_position).set_weights([
        _loader('bert/embeddings/position_embeddings')[:config['max_position_len'], :],
    ])
    model.get_layer(name=layer_name.embedding_norm).set_weights([
        _loader('bert/embeddings/LayerNorm/gamma'),
        _loader('bert/embeddings/LayerNorm/beta'),
    ])

    for block_index in range(config['n_transformer_block']):
        weight_prefix = 'bert/encoder/layer_%d/' % block_index
        model.get_layer(name=getattr(layer_name, 'transformer_%s_attention' % block_index)).set_weights([
            _loader(weight_prefix + 'attention/self/query/kernel'),
            _loader(weight_prefix + 'attention/self/query/bias'),
            _loader(weight_prefix + 'attention/self/key/kernel'),
            _loader(weight_prefix + 'attention/self/key/bias'),
            _loader(weight_prefix + 'attention/self/value/kernel'),
            _loader(weight_prefix + 'attention/self/value/bias'),
            _loader(weight_prefix + 'attention/output/dense/kernel'),
            _loader(weight_prefix + 'attention/output/dense/bias'),
        ])
        model.get_layer(name=getattr(layer_name, 'transformer_%s_attention_norm' % block_index)).set_weights([
            _loader(weight_prefix + 'attention/output/LayerNorm/gamma'),
            _loader(weight_prefix + 'attention/output/LayerNorm/beta'),
        ])
        model.get_layer(name=getattr(layer_name, 'transformer_%s_feed_forward' % block_index)).set_weights([
            _loader(weight_prefix + 'intermediate/dense/kernel'),
            _loader(weight_prefix + 'intermediate/dense/bias'),
            _loader(weight_prefix + 'output/dense/kernel'),
            _loader(weight_prefix + 'output/dense/bias'),
        ])
        model.get_layer(name=getattr(layer_name, 'transformer_%s_feed_forward_norm' % block_index)).set_weights([
            _loader(weight_prefix + 'output/LayerNorm/gamma'),
            _loader(weight_prefix + 'output/LayerNorm/beta'),
        ])

    model.get_layer(name=layer_name.pooler_dense).set_weights([
        _loader('bert/pooler/dense/kernel'),
        _loader('bert/pooler/dense/bias'),
    ])
    model.get_layer(name=layer_name.mlm_dense).set_weights([
        _loader('cls/predictions/transform/dense/kernel'),
        _loader('cls/predictions/transform/dense/bias'),
    ])
    model.get_layer(name=layer_name.mlm_norm).set_weights([
        _loader('cls/predictions/transform/LayerNorm/gamma'),
        _loader('cls/predictions/transform/LayerNorm/beta'),
    ])
    model.get_layer(name=layer_name.mlm_softmax).set_weights([
        _loader('cls/predictions/output_bias'),
    ])
    model.get_layer(name=layer_name.nsp_softmax).set_weights([
        np.transpose(_loader('cls/seq_relationship/output_weights')),
        _loader('cls/seq_relationship/output_bias'),
    ])
