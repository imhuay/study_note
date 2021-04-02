#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-04-02 5:54 下午
    
Author:
    huayang
    
Subject:
    
"""

from basic_utils import SerializeUtils


if __name__ == '__main__':
    """"""
    test_file = r'data/pok.jpg'
    test_file_cp = r'data/-pok_cp.jpg'

    # bytes to str
    b = open(test_file, 'rb').read()
    s = SerializeUtils.bytes_to_str(b)
    print(s[:10])

    # str to bytes
    b2 = SerializeUtils.str_to_bytes(s)
    print(b == b2)

    # file to str
    s2 = SerializeUtils.file_to_str(test_file)
    print(s == s2)

    # str to file
    SerializeUtils.str_to_file(s, test_file_cp)
