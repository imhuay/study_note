#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-03-09 10:42
    
Author:
    huayang
    
Subject:
    任意对象的序列化与反序列化
"""
import base64


def file_to_str(file_path: str, encoding='utf8') -> str:
    with open(file_path, 'rb') as fp:
        return bytes_to_str(fp.read(), encoding=encoding)


def str_to_file(s: str, file_path: str, encoding='utf8') -> None:
    with open(file_path, 'wb') as fp:
        fp.write(str_to_bytes(s, encoding))


def bytes_to_str(b: bytes, encoding='utf8') -> str:
    return base64.b64encode(b).decode(encoding)


def str_to_bytes(s: str, encoding='utf8') -> bytes:
    return base64.b64decode(s.encode(encoding))


def _test_all():
    test_file = r'./_test_data/pok.jpg'
    test_file_cp = r'./-out/pok_cp.jpg'

    # bytes to str
    b = open(test_file, 'rb').read()
    s = bytes_to_str(b)
    print(s[:10])

    # str to bytes
    b2 = str_to_bytes(s)
    assert b == b2

    # file to str
    s2 = file_to_str(test_file)
    assert s == s2

    # str to file
    str_to_file(s, test_file_cp)
    assert open(test_file, 'rb').read() == open(test_file_cp, 'rb').read()


if __name__ == '__main__':
    """"""
    _test_all()