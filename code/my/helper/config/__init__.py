#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-04-01 8:58 下午
    
Author:
    huayang
    
Subject:
    一个用于加载配置文件的装饰器，可用于代替 argparse
"""

from .bunch import Bunch
from .base_config import BaseConfig

from my.decorators import load_config
