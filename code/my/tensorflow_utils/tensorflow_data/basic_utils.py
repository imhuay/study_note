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
import tensorflow as tf


def split(*arrays, val_size=0.25, random_seed=1, shuffle=False):
    """
    将数据按比例切分

    Args:
        *arrays:
        val_size: 切分比例
        random_seed: 随机数种子
        shuffle: 是否打乱

    Examples:
        (a_train, b_train, c_train), (a_val, b_train, c_train) = split(a, b, c)
    """
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


def build_dataset(data,
                  batch_size=8,
                  map_func=None,
                  shuffle=False,
                  n_repeat=None,
                  n_parallel=None,
                  prefetch=True,
                  random_seed=1,
                  drop_remainder=False,
                  reshuffle_each_iteration=None,
                  buffer_size=None):
    """"""
    ds = tf.data.Dataset.from_tensor_slices(data)

    if buffer_size is None:
        buffer_size = batch_size * 10

    if map_func:
        ds = ds.map(map_func, num_parallel_calls=n_parallel)

    if shuffle:  # 是否打乱
        ds = ds.shuffle(buffer_size, seed=random_seed, reshuffle_each_iteration=reshuffle_each_iteration)

    ds = ds.batch(batch_size=batch_size, drop_remainder=drop_remainder)

    # 建议先 batch 再 repeat
    if n_repeat:
        ds = ds.repeat(n_repeat)

    if prefetch:  # 预加载，使用 GPU 训练时有用
        ds = ds.prefetch(buffer_size)
    return ds
