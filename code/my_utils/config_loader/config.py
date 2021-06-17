#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-06-09 9:02 下午
    
Author:
    huayang
    
Subject:
    
"""


class BaseConfig:
    """"""

    def __init__(self, **kwargs):
        """"""
        for k, v in kwargs.items():
            if k not in self.__dict__:
                raise ValueError(f'No such config item: {k}')
            setattr(self, k, v)


class BertConfig(BaseConfig):
    """"""

    def __init__(self, **kwargs):
        """"""
        self.attention_probs_dropout_prob = 0.1
        self.directionality = 'bidi'
        self.hidden_act = 'gelu'
        self.hidden_dropout_prob = 0.1
        self.hidden_size = 768
        self.initializer_range = 0.02
        self.intermediate_size = 3072
        self.max_position_embeddings = 512
        self.num_attention_heads = 12
        self.num_hidden_layers = 12
        self.pooler_fc_size = 768
        self.pooler_num_attention_heads = 12
        self.pooler_num_fc_layers = 3
        self.pooler_size_per_head = 128
        self.pooler_type = 'first_token_transform'
        self.type_vocab_size = 2
        self.vocab_size = 21128

        super(BertConfig, self).__init__(**kwargs)


if __name__ == '__main__':
    """"""
    cfg = BertConfig(num_attention_heads=6, num_hidden_layers=6)
    print(cfg.num_attention_heads)  # 6
    print(cfg.num_hidden_layers)  # 6

    cfg = BertConfig(sth=6)  # ValueError: No such config item: sth
