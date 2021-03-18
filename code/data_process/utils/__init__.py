#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-03-18 5:06 下午
    
Author:
    huayang
    
Subject:

"""

from .data_split import split


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


if __name__ == '__main__':
    """"""
    import sklearn.model_selection as ms
    ms.train_test_split()

