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
        self._replacement_map = {}  # 缓存

    def default(self, o):
        if isinstance(o, NoIndent):
            # key = uuid.uuid4().hex  # 慢
            self._replacement_map[id(o)] = json.dumps(o.value, **self.kwargs)
            return self.FORMAT_SPEC.format(id(o))
        else:
            return super(NoIndentEncoder, self).default(o)

    def encode(self, o):
        result = super(NoIndentEncoder, self).encode(o)
        for k, v in self._replacement_map.items():
            result = result.replace('"{}"'.format(self.FORMAT_SPEC.format(k)), v)
        return result


if __name__ == '__main__':
    """"""
    # 示例 1
    json_data = {}
    grid_list = [["a", "一"], ["b", "二"]]
    for did, it in zip(["1", "2"], grid_list):
        json_data[did] = NoIndent(it)

    json_data = json.dumps(json_data, cls=NoIndentEncoder, ensure_ascii=False, sort_keys=True, indent=4)
    print(json_data)
    """
    {
        "1": ["a", "一"],
        "2": ["b", "二"]
    }
    """

    # 示例 2
    json_data = {}
    grid_list = [["a", "一"], ["b", "二"]]
    for did, iid, it in zip(["1", "2"], ['A', 'B'], grid_list):
        # tmp = {iid: NoIndent(it)}  # err，NoIndent 不能嵌套，只需要包在最外层
        tmp = {iid: it}
        json_data[did] = NoIndent(tmp)

    json_data = json.dumps(json_data, cls=NoIndentEncoder, ensure_ascii=False, sort_keys=True, indent=4)
    print(json_data)
