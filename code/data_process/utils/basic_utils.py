#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-03-16 7:30 下午
    
Author:
    huayang
    
Subject:
    
"""

import numpy as np


def split(*arrays, val_size=0.2, random_seed=1, shuffle=False):
    """"""
    arrays = [np.asarray(x) for x in arrays]

    # assert
    lens = [len(x) for x in arrays]
    if len(np.unique(lens)) > 1:
        raise ValueError('The length of each array must be same, but %r.' % lens)

    n_sample = lens[0]
    n_val = int(np.ceil(val_size * n_sample))

    if shuffle:
        arr_zip = list(zip(*arrays))
        rs = np.random.RandomState(random_seed)
        rs.shuffle(arr_zip)
        arrays = [list(x) for x in zip(*arr_zip)]

    arr_val = [x[-n_val:] for x in arrays]
    arr_train = [x[:-n_val] for x in arrays]

    return arr_train, arr_val

