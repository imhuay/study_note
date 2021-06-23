#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-04-06 5:35 下午
    
Author:
    huayang
    
Subject:

"""

from data_utils import image_utils

# ret = image_utils.Tensorize.by_pil(r'data/pok.jpg')
ret = image_utils.Tensorize.by_pil(r'data/pok.jpg')
print(ret.shape)
