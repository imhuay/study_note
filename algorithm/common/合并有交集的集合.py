#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-05-17 9:21 下午
    
Author:
    huayang
    
Subject:
    
"""
from typing import List, Set


def merge_sets(src: List[Set]):
    """"""
    pool = set(map(frozenset, src))  # 去重
    groups = []
    while pool:
        groups.append(set(pool.pop()))
        while True:
            for s in pool:
                if groups[-1] & s:
                    groups[-1] |= s
                    pool.remove(s)
                    break
            else:
                break
    return groups


if __name__ == '__main__':
    """"""
    _src = [{1, 3}, {2, 3}, {4, 5}, {4, 5}, {6, 5}, {7, 5}, {8, 9}, {8, 9}]
    ret = merge_sets(_src)
    print(ret)
