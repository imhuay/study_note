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
            setattr(self, k, v)
