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


class Serializer:
    """"""

    @staticmethod
    def file_to_str(file_path, encoding='utf8'):
        with open(file_path, 'rb') as fp:
            return Serializer.byte_to_str(fp.read(), encoding=encoding)

    @staticmethod
    def byte_to_str(byte_obj, encoding='utf8'):
        return base64.b64encode(byte_obj).decode(encoding)

    @staticmethod
    def str_to_byte(byte_str, encoding='utf8'):
        return base64.b64decode(byte_str.encode(encoding))


if __name__ == '__main__':
    """"""
    # 文本文件
    obj = open('basic_utils/-data/test.txt', 'rb').read()
    s = Serializer.byte_to_str(obj)
    obj_str = Serializer.str_to_byte(s)
    with open('basic_utils/-out/test.txt', 'wb') as f:
        f.write(obj_str)

    # 图片
    obj = open('basic_utils/-data/pok.jpg', 'rb').read()
    s = Serializer.byte_to_str(obj)
    obj_str = Serializer.str_to_byte(s)
    with open('basic_utils/-out/pok.jpg', 'wb') as f:
        f.write(obj_str)

    # 视频
    obj = open('basic_utils/-data/v_ApplyEyeMakeup_g01_c01.avi', 'rb').read()
    s = Serializer.byte_to_str(obj)
    obj_str = Serializer.str_to_byte(s)
    with open('basic_utils/-out/v_ApplyEyeMakeup_g01_c01.avi', 'wb') as f:
        f.write(obj_str)

    s = Serializer.file_to_str(r'basic_utils/-data/14522667.jpg')
    print(len(s))
    with open('basic_utils/-out/14522667.txt', 'w') as f:
        f.write(s)
