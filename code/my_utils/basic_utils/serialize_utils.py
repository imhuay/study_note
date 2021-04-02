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


class SerializeUtils:
    """"""

    @staticmethod
    def file_to_str(file_path: str, encoding='utf8') -> str:
        with open(file_path, 'rb') as fp:
            return _bytes_to_str(fp.read(), encoding=encoding)

    @staticmethod
    def str_to_file(s: str, file_path: str, encoding='utf8') -> None:
        with open(file_path, 'wb') as fp:
            fp.write(_str_to_bytes(s, encoding))

    @staticmethod
    def bytes_to_str(b: bytes, encoding='utf8') -> str:
        return _bytes_to_str(b, encoding)

    @staticmethod
    def str_to_bytes(s: str, encoding='utf8') -> bytes:
        return _str_to_bytes(s, encoding)


def _bytes_to_str(b: bytes, encoding='utf8'):
    return base64.b64encode(b).decode(encoding)


def _str_to_bytes(s: str, encoding='utf8'):
    return base64.b64decode(s.encode(encoding))
