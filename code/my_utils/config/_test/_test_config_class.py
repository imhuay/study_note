#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-06-18 5:13 下午
    
Author:
    huayang
    
Subject:
    
"""

from my_utils.config import BaseConfig, load_config


class TestConfig(BaseConfig):
    """"""
    def __init__(self, **kwargs):
        """"""
        self.item_a = 'a'
        self.item_b = 'b'
        self.item_c = 'c'
        # self.item_d = 'd'

        super(TestConfig, self).__init__(**kwargs)


@load_config('./test_config_class.yaml', config_cls=TestConfig)
def main(cfg: TestConfig):
    """
    test_config_class.yaml
        item_a: A
        item_b: B
        item_d: D  # 会报错，因为对应的配置类中没有该项
    """
    print(cfg.item_a)
    print(cfg.item_b)
    print(cfg)


if __name__ == '__main__':
    """"""
    main()
