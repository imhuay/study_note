#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-06-08 4:30 下午
    
Author:
    huayang
    
Subject:
    自定义 json 格式输出，对指定对象不进行缩进

    示例：
    ```
    {
        "1": ["a", "一"],  # 这里的列表没有缩进
        "2": ["b", "二"]
    }
    ```
"""

import json
from _ctypes import PyObj_FromPtr


class NoIndent(object):
    """ Value wrapper. """

    def __init__(self, value):
        self.value = value


class NoIndentEncoder(json.JSONEncoder):
    FORMAT_SPEC = '@@{}@@'

    def __init__(self, *args, **kwargs):
        super(NoIndentEncoder, self).__init__(*args, **kwargs)
        self.kwargs = kwargs
        del self.kwargs['indent']
        # self._replacement_map = {}  # 缓存 id(obj) -> obj
        self._no_indent_obj_ids = set()  # 使用 PyObj_FromPtr，保存 id(obj) 即可

    def default(self, o):
        if isinstance(o, NoIndent):
            # self._replacement_map[id(o)] = json.dumps(o.value, **self.kwargs)
            self._no_indent_obj_ids.add(id(o))
            return self.FORMAT_SPEC.format(id(o))
        else:
            return super(NoIndentEncoder, self).default(o)

    def encode(self, o):
        result = super(NoIndentEncoder, self).encode(o)

        # for oid, tmp_str in self._replacement_map.items():
        for oid in self._no_indent_obj_ids:
            tmp_str = json.dumps(PyObj_FromPtr(oid).value, **self.kwargs)
            result = result.replace('"{}"'.format(self.FORMAT_SPEC.format(oid)), tmp_str)
        return result
