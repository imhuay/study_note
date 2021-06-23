#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-06-21 4:42 下午
    
Author:
    huayang
    
Subject:
    list 相关的常用操作
"""


def unique_list(ls):
    """列表去重"""
    return list(set(ls))


def unique_list_sorted(ls):
    """列表去重，不改变顺序"""
    tmp = unique_list(ls)
    tmp.sort(key=ls.index)
    return tmp
