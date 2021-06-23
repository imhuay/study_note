#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-06-23 5:07 下午
    
Author:
    huayang
    
Subject:
    
"""
import functools
from typing import Callable

from my_utils.basic import multi_thread_wrapper


def run_multi_thread(args, **kwargs):
    """
    多线程执行装饰器

    Args:
        args: 参数序列，也可以是一个函数，返回需要的参数序列
        kwargs: 详见 multi_thread_wrapper 相关参数
    """
    def decorator(func):

        @functools.wraps(func)
        def decorated_func():
            _args = args() if isinstance(args, Callable) else args
            return multi_thread_wrapper(func, _args, **kwargs)

        return decorated_func

    return decorator


def _test_simple():
    """"""

    def get_args():
        return list([(str(i), str(i+1)) for i in range(1000)])

    @run_multi_thread(get_args, star_args=True)
    def some_func(s, x):
        """一个简单的测试函数，输入 s 加一个后缀"""
        # time.sleep(math.sqrt(int(s)))
        return s + '-' + x

    ret = some_func()
    print(ret)

    args = list([(str(i), str(i + 1)) for i in range(1000)])

    @run_multi_thread(args)
    def some_func_x(a):
        s, x = a[0], a[1]
        return s + '-' + x

    ret_x = some_func_x()
    assert ret_x == ret


if __name__ == '__main__':
    """"""

    _test_simple()
