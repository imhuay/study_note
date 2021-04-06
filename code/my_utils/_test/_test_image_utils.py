#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-04-06 5:35 下午
    
Author:
    huayang
    
Subject:
    
"""

import data_utils as du

import data_utils
# import data_utils.image_utils as image_utils
from data_utils import image_utils
# from data_utils.image_utils import Tensorize

# ret = image_utils.Tensorize.by_pil(r'data/pok.jpg')
ret = image_utils.Tensorize.by_pil(r'data/pok.jpg')
print(ret)
