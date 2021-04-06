#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-04-02 7:06 下午
    
Author:
    huayang
    
Subject:
    
"""
import numpy as np


def safe_indexing(x, indices=None):
    """
    Return items or rows from X using indices.

    Args:
        x:
        indices:

    References:
        sklearn.utils.safe_indexing
    """
    if indices is None:
        return x

    if hasattr(x, "shape"):  # for numpy
        try:
            return x.take(indices, axis=0)  # faster
        except:
            return x[indices]
    elif hasattr(x, "iloc"):  # for pandas
        indices = indices if indices.flags.writeable else indices.copy()
        try:
            return x.iloc[indices]
        except:
            return x.copy().iloc[indices]
    else:  # for python
        return [x[idx] for idx in indices]


def split(*arrays, split_size=0.25, random_seed=1, shuffle=True):
    """
    将数据按比例切分

    Args:
        *arrays:
        split_size: 切分比例
        random_seed: 随机数种子
        shuffle: 是否打乱

    Examples:
        (a_train, b_train, c_train), (a_val, b_train, c_train) = split(a, b, c)

        >>> x = [[i] * 128 for i in range(100)]
        >>> y = list(range(100))
        >>> (x_t, y_t), (x_v, y_v) = split(x, y)
        >>> (np.asarray(x_t)[:5, 0] == np.asarray(y_t)[:5]).all()
        True
    """
    # assert
    lens = [len(x) for x in arrays]
    if len(set(lens)) > 1:
        raise ValueError('The length of each array must be same, but %r.' % lens)

    n_sample = lens[0]
    n_val = int(np.ceil(split_size * n_sample))

    if shuffle:
        rs = np.random.RandomState(random_seed)
        idx = rs.permutation(n_sample)
    else:
        idx = np.arange(n_sample)

    idx_val = idx[-n_val:]
    idx_train = idx[:-n_val]
    arr_val = [safe_indexing(x, idx_val) for x in arrays]
    idx_val = [safe_indexing(x, idx_train) for x in arrays]

    return idx_val, arr_val
