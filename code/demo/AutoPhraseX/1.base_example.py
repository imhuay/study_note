#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-04-15 2:34 下午
    
Author:
    huayang
    
Subject:

References:
    https://github.com/luozhouyang/AutoPhraseX
"""


def _base():
    """"""
    from autophrasex import AutoPhrase, BaiduLacTokenizer, Strategy, JiebaTokenizer
    tokenizer = BaiduLacTokenizer()
    strategy = Strategy(
        tokenizer=tokenizer,
        N=4,
        threshold=0.45,
        threshold_schedule_factor=1.0)

    autophrase = AutoPhrase()
    predictions = autophrase.mine(
        input_doc_files=['./data/docs/t.txt'],
        quality_phrase_files=['/path/to/quality/phrase'],
        strategy=strategy,
        N=4,
        epochs=10)

    for pred in predictions:
        print(pred)


def _test_NgramsCallback():
    """"""
    from autophrasex import NgramsCallback
    nc = NgramsCallback()
    nc.update_ngrams()
    ret = nc.pmi_of("中国 雅虎")
    print(ret)


if __name__ == '__main__':
    """"""
    # _test_NgramsCallback()
    _base()
