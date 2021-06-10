#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-06-08 4:39 下午
    
Author:
    huayang
    
Subject:
    
"""

import json

from my_utils.json_encoder.no_indent import NoIndent, NoIndentEncoder


def _test_no_indent():
    """"""
    fw_1 = open(r'./_test_output_1.json', 'w', encoding='utf8')
    fw_2 = open(r'./_test_output_2.json', 'w', encoding='utf8')

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
