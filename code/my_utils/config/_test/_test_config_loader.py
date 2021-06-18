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
from my_utils.config import load_config


@load_config()
def main1(cfg):
    """"""
    print(cfg.a)
    print(cfg.b)
    print(cfg.b.c)


@load_config('test_config.yaml', file_type='yaml')
def main2(cfg):
    """"""
    print(cfg.a)
    print(cfg.b)
    print(cfg.b.c)


def main3():
    """"""
    from my_utils.config.config import BaseConfig

    class TestConfig(BaseConfig):
        """"""
        def __init__(self, **kwargs):
            self.a = None
            self.b = None
            super(TestConfig, self).__init__(**kwargs)

    @load_config('test_config.json', config_cls=TestConfig)
    def test3(cfg: TestConfig):
        print(cfg.a)
        print(cfg.b)
        print(cfg.b['c'])

    test3()


if __name__ == '__main__':
    """"""
    print('main1:')
    sys.argv = ['', 'test_config.json']
    main1()
    """
    1
    {'c': 2, 'd': {'e': 3}}
    2
    """
    print()

    print('main2:')
    main2()
    print()

    print('main3:')
    main3()
    print()
