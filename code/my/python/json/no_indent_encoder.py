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


def _test_no_indent():
    """"""
    import os
    os.makedirs('./-out', exist_ok=True)

    fw_1 = open(r'./-out/_test_output_1.json', 'w', encoding='utf8')
    fw_2 = open(r'./-out/_test_output_2.json', 'w', encoding='utf8')

    json_data_1 = {}
    json_data_2 = {}
    grid_list = [["a", "一"], ["b", "二"]]
    for did, iid, it in zip(["1", "2"], ['A', 'B'], grid_list):
        json_data_1[did] = {iid: NoIndent(it)}
        json_data_2[did] = NoIndent({iid: it})
        # json_data_2[did] = NoIndent({iid: NoIndent(it)})  # err，NoIndent 不能嵌套，只需要包在最外层

    json_data_1 = json.dumps(json_data_1, cls=NoIndentEncoder, ensure_ascii=False, sort_keys=True, indent=4)
    fw_1.write(json_data_1)
    json_data_2 = json.dumps(json_data_2, cls=NoIndentEncoder, ensure_ascii=False, sort_keys=True, indent=4)
    fw_2.write(json_data_2)

    print(json_data_1)
    """
    {
        "1": {
            "A": ["a", "一"]
        },
        "2": {
            "B": ["b", "二"]
        }
    }
    """

    print(json_data_2)
    """
    {
        "1": {"A": ["a", "一"]},
        "2": {"B": ["b", "二"]}
    }
    """


if __name__ == '__main__':
    _test_no_indent()