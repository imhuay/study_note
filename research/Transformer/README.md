Transformer 模型族
===

Index
---
<!-- TOC -->

- [Transformer](#transformer)
    - [Transformer 改进](#transformer-改进)
- [BERT 相关](#bert-相关)
    - [RoBERTa](#roberta)
        - [中文 RoBERTa](#中文-roberta)
    - [SentenceBERT](#sentencebert)

<!-- /TOC -->


## Transformer
- 【2017】[Attention Is All You Need](https://arxiv.org/abs/1706.03762)
    > 提出 Transformer 结构

### Transformer 改进
- 【2020】[On Layer Normalization in the Transformer Architecture](https://arxiv.org/abs/2002.04745)
    > 分析了 PerLN 和 PostLN 的优缺点：
    > - PreLN 对梯度下降更友好，收敛更快，对超参数更鲁棒，但性能一般弱于 PostLN；
    > - PostLN 更难训练，需要从一个较小的学习率开始，配合预热（warm-up）进行训练；

<div align="center"><img src="./_assets/PostLN和PreLN图示.png" height="300" /></div>

- 【2020】[RealFormer: Transformer Likes Residual Attention](https://arxiv.org/abs/2012.11747)
    > 兼顾 PostLN 的性能和 PreLN 的稳定
    - 【解读】[RealFormer：把残差转移到Attention矩阵上面去 - 科学空间](https://kexue.fm/archives/8027)
- 【2020】[ReZero is All You Need: Fast Convergence at Large Depth](https://arxiv.org/abs/2003.04887)
    > 针对残差结构的优化：$x+f(x)$ → $x+αf(x)$，主要用于加速收敛，论文表明可以代替 Transformer 中的 LayerNorm 层
    - 【Github】[Official PyTorch Repo for "ReZero is All You Need: Fast Convergence at Large Depth"](https://github.com/majumderb/rezero)
- 实现
    - 【pytorch】[The Annotated Transformer](http://nlp.seas.harvard.edu/2018/04/03/attention.html)
        > 这里使用的是 PerLN，官方实现为 PostLN


## BERT 相关

### RoBERTa
> 【2019】[RoBERTa: A Robustly Optimized BERT Pretraining Approach](https://arxiv.org/abs/1907.11692)

**模型小结**
> [RoBERTa 详解 - 知乎](https://zhuanlan.zhihu.com/p/103205929)
- 模型结构与 BERT 相同；
- 动态 mask：每次将训练数据喂给模型时，才进行随机mask；
    > 静态 mask：将一个样本复制 `dupe_factor` 次，每次 mask 不同的 token；且不同的 mask 会输入不同的 epoch；
    >> 例：`dupe_factor=10`，`epoch=40`，则每种 mask 的方式在训练中会被使用4次。
- 以 Doc-Sentences 的方式构建语料，并移除 Next Sentence Prediction loss；
    > Doc-Sentences: 使用来自一篇 doc 中的连续句子作为单个样本，token 数量不超过 512；
    >> 论文比较了 4 种语料构建方式：1）Segment-Pair；2）Sentence-Pair；3）Full-Sentences；4）Doc-Sentences，详见原文；
- 更多训练数据、更大 batch size、更长训练时间；

#### 中文 RoBERTa
> [RoBERTa 中文预训练模型: RoBERTa for Chinese](https://github.com/brightmart/roberta_zh)
>> 没有实现动态 mask，而是通过增大样本复制数量（`dupe_factor`参数）达到类似的效果；


### SentenceBERT
> 【2019】[Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://arxiv.org/abs/1908.10084)
>> 句向量、孪生网络；语义相似度计算、聚类

