#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-06-23 9:00 下午
    
Author:
    huayang
    
Subject:
    系统相关的常用操作
"""
import platform


def get_system():
    """获取当前系统类型"""
    return platform.system()


def _system_is(sys_name):
    """"""
    return get_system() == sys_name


def is_linux():
    """判断是否为 linux 系统"""
    return _system_is('Linux')


def is_windows():
    """判断是否为 windows 系统"""
    return _system_is('Windows')


def is_mac():
    """判断是否为 mac os 系统"""
    return _system_is('Darwin')


def _test():
    """"""
    assert is_mac()


if __name__ == '__main__':
    """"""
    _test()