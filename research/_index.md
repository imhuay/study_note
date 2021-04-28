关键词索引
===
深度学习、机器学习、数据挖掘等

Index
---
<!-- TOC -->

- [机器学习、深度学习](#机器学习深度学习)
    - [优化算法](#优化算法)
    - [度量学习](#度量学习)
- [数据挖掘](#数据挖掘)
- [NLP](#nlp)
    - [开源库](#开源库)
    - [Transformer 系列模型](#transformer-系列模型)
        - [BERT 及其变种](#bert-及其变种)
        - [BERT 实践](#bert-实践)
    - [关键词挖掘](#关键词挖掘)
    - [小样本学习（NLP）](#小样本学习nlp)
        - [数据增强（扩充）](#数据增强扩充)
        - [数据增强（融合）](#数据增强融合)
    - [TODO](#todo)
- [开源库](#开源库-1)
    - [TensorFlow](#tensorflow)
    - [Keras](#keras)
    - [PyTorch](#pytorch)

<!-- /TOC -->


## 机器学习、深度学习

### 优化算法
> 优化器、optimizer

- Adam
- AdamW、权重衰减
    - 【论文】 [Decoupled Weight Decay Regularization](https://arxiv.org/abs/1711.05101)
    - [比较 Adam 和 AdamW - TFknight](https://www.cnblogs.com/tfknight/p/13425532.html)


### 度量学习
> Metric Learning、距离度量学习 (Distance Metric Learning，DML) 、相似度学习

- 【开源库】[pytorch for metric learning](https://github.com/KevinMusgrave/pytorch-metric-learning)


## 数据挖掘


## NLP

### 开源库
- [huggingface/transformers](https://github.com/huggingface/transformers)

### Transformer 系列模型
- Transformer
    - 代码
        - 【pytorch】[The Annotated Transformer](http://nlp.seas.harvard.edu/2018/04/03/attention.html)
#### BERT 及其变种
- BERT
    - 【官方源码、tf1】[google-research/bert](https://github.com/google-research/bert)
    - 【pytorch】 [codertimo/BERT-pytorch](https://github.com/codertimo/BERT-pytorch)
    - 【pytorch】[huggingface/transformers/bert](https://github.com/huggingface/transformers/blob/master/src/transformers/models/bert/modeling_bert.py)
    - 【tf2】[huggingface/transformers/bert](https://github.com/huggingface/transformers/blob/master/src/transformers/models/bert/modeling_tf_bert.py)

- RoBERTa
    - 【论文】
    - 【解读】[RoBERTa 详解 - 知乎](https://zhuanlan.zhihu.com/p/103205929)
    
- StructBERT
    - 【论文】[StructBERT: Incorporating Language Structures into Pre-training for Deep Language Understanding](https://arxiv.org/abs/1908.04577)
    - 【解读】[StructBERT解读_fengzhou-CSDN博客](https://blog.csdn.net/fengzhou_/article/details/107028168)

#### BERT 实践
- 【BERT for NER】[基于BERT预训练的中文命名实体识别TensorFlow实现_macanv的专栏-CSDN博客_bert中文命名实体识别](https://blog.csdn.net/macanv/article/details/85684284)
- 【BERT for 小样本学习】[必须要GPT3吗？不，BERT的MLM模型也能小样本学习 - 科学空间|Scientific Spaces](https://spaces.ac.cn/archives/7764)


### 关键词挖掘
- [NLP关键词提取方法总结及实现-CSDN博客](https://blog.csdn.net/asialee_bird/article/details/96454544)


### 小样本学习（NLP）
> Few-Shot Learning、Zero-Shot Learning

#### 数据增强（扩充）

#### 数据增强（融合）


### TODO
- 文本蕴含


## 开源库

### TensorFlow
- 【官方文档】[TensorFlow Tutorials](https://www.tensorflow.org/tutorials)


### Keras
- 【官方文档】[Keras API reference](https://keras.io/api/)


### PyTorch
- 【官方文档】[PyTorch Tutorials](https://pytorch.org/tutorials/beginner/basics/intro.html)