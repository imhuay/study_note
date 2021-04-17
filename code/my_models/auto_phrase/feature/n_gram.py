#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-04-16 3:09 下午
    
Author:
    huayang
    
Subject:
    
"""
import math

from operator import mul
from functools import reduce
from collections import Counter


# class NGram(object):
#     """"""
#
#     def __init__(self, n=4, epsilon=1e-5):
#         """"""
#         self.epsilon = epsilon
#         self.N = n
#         self.ngrams_freq = dict()  #

class NGramFeature(object):

    def __init__(self, n=4, epsilon=1e-5):
        self.epsilon = epsilon
        self.n = n
        self.ngrams_freq = {i: Counter() for i in range(1, self.n + 1)}
        self.ngram_total_occur = {i: 0 for i in range(1, self.n + 1)}
        self.update_flag = False

    def update(self, ngram: tuple, n: int):
        # if filter_fn(ngram): return  # 放到最外层
        self.ngrams_freq[n][ngram] += 1
        self.update_flag = True

    def update_occur(self):
        """"""
        if self.update_flag:
            self.ngram_total_occur = {i: sum(self.ngrams_freq[i].values()) for i in range(1, self.n + 1)}
            self.update_flag = False

    def _pmi_of(self, ngram: tuple, n: int, freq: int, unigram_total_occur: int, ngram_total_occur: int):
        joint_prob = freq / (ngram_total_occur + self.epsilon)
        indep_prob = reduce(mul, [self.ngrams_freq[1][unigram] for unigram in ngram]) / (unigram_total_occur ** n)
        pmi = math.log((joint_prob + self.epsilon) / (indep_prob + self.epsilon), 2)
        return pmi

    def pmi_of(self, ngram: tuple):
        n = len(ngram)
        if n not in self.ngrams_freq:
            return 0.0

        self.update_occur()
        freq = self.ngrams_freq[n].get(ngram, 0)
        return self._pmi_of(ngram, n, freq, self.ngram_total_occur[1], self.ngram_total_occur[n])

    def pmi(self):
        pmi_dict = dict()
        self.update_occur()
        for n in range(2, self.n + 1):
            for ngram, freq in self.ngrams_freq[n].items():
                pmi_dict[ngram] = self._pmi_of(ngram, n, freq, self.ngram_total_occur[1], self.ngram_total_occur[n])
        return dict(sorted(pmi_dict.items(), key=lambda x: -x[1]))
