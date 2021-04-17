#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-04-16 3:11 下午
    
Author:
    huayang
    
Subject:
    
"""

import re

from .config_utils import load_config

from autophrasex.utils import STOPWORDS

STOPWORDS = STOPWORDS.stopwords_set
CHINESE_PATTERN = re.compile(r'^[0-9a-zA-Z\u4E00-\u9FA5]+$')
CHARACTERS = set('!"#$%&\'()*+,-./:;?@[\\]^_`{|}~ \t\n\r\x0b\x0c，。？：“”【】「」')


def ngram_yield(sequence, n=2):
    start = 0
    end = start + n
    while end <= len(sequence):
        yield (start, end), tuple(sequence[start: end])
        start += 1
        end = start + n


def ngram_filter(ngram):
    """"""
    if any(x in CHARACTERS for x in ngram):
        return True
    if any(x in STOPWORDS for x in ngram):
        return True
    if CHINESE_PATTERN.match(''.join(ngram)):
        return False
    return True
