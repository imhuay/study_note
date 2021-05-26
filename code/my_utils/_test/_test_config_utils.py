#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-04-01 8:11 下午
    
Author:
    huayang
    
Subject:
    
"""

import sys
from config_utils import load_config


@load_config()
def main1(cfg):
    """"""
    print(type(cfg))
    print(cfg)


@load_config('test_config.yaml', file_type='yaml')
def main2(cfg):
    """"""
    print(type(cfg))
    print(cfg)


if __name__ == '__main__':
    """"""
    sys.argv = ['', 'test_config.json']
    # print(sys.argv)

    main1()
    """
    <class 'basic_utils.config.bunch.Bunch'>
    {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}
    """

    main2()

