#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-04-16 4:18 下午
    
Author:
    huayang
    
Subject:
    
"""


from feature.n_gram import NGramFeature
from autophrasex import BaiduLacTokenizer

from utils import ngram_yield, ngram_filter

t = BaiduLacTokenizer()

ng = NGramFeature()

# line = "北京时间 4 月 15 日晚间消息，据报道，一名联邦法官今日驳回了联邦陪审团之前作出的，要求苹果赔偿 5.062 亿美元的裁决。"
# for it in ngram_yield(line, 3):
#     print(it)  # (start, end), ngram

with open('../data/docs/t.txt', encoding='utf8') as f:
    for line in f:
        line = line.rstrip('\n')

        tokens = t.tokenize(line)
        for n in range(1, 5):
            for _, ngram in ngram_yield(tokens, n):
                if ngram_filter(ngram):
                    continue
                ng.update(ngram, n)

        ng.update_occur()

print(ng)




