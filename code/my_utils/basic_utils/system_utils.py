#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-02-04 14:35
    
Author:
    huayang
    
Subject:
    
"""
import platform


class SystemUtils:

    @staticmethod
    def get_system():
        """获取当前系统类型"""
        return _get_system()

    @staticmethod
    def system_is(sys_name):
        """"""
        return _system_is(sys_name)

    @staticmethod
    def is_linux():
        """判断是否为 linux 系统"""
        return _system_is('Linux')

    @staticmethod
    def is_windows():
        """判断是否为 windows 系统"""
        return _system_is('Windows')

    @staticmethod
    def is_mac():
        """判断是否为 mac os 系统"""
        return _system_is('Darwin')


def _get_system():
    """获取当前系统类型"""
    return platform.system()


def _system_is(sys_name):
    """"""
    return _get_system() == sys_name
