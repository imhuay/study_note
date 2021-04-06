#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-04-01 7:23 下午
    
Author:
    huayang
    
Subject:
    一个用于加载配置文件的装饰器，参考自 facebook 的开源库 hydra 的一种典型使用场景。

    ```
    import hydra

    @hydra.main(config_name="config.yaml")
    def main(cfg):
        ...
    ```

References:
    facebookresearch/hydra | https://github.com/facebookresearch/hydra
"""
import os
import sys
import json
import functools

from ._bunch import Bunch

ALLOW_FILE_TYPE = {'json', 'yaml'}


def _load_config_json(config_path):
    with open(config_path) as fp:
        config = Bunch.from_dict(json.load(fp))
    return config


def _load_config_yaml(config_path):
    try:
        import yaml
    except:
        raise ValueError('No yaml lib, please `pip install pyyaml`.')

    with open(config_path) as fp:
        config = Bunch.from_dict(yaml.safe_load(fp.read()))
    return config


def _load_config_file(file_path, file_type):
    """"""
    argv = sys.argv
    if file_path is None:
        if len(argv) < 2:
            raise ValueError('Config file path must be given, at parameter or command line.')
        file_path = sys.argv[1]

    if file_type is None:
        if len(argv) > 2:  # 如果在命令行指定了 file_type
            file_type = sys.argv[2]
        else:  # 看文件后缀
            _, ext = os.path.splitext(file_path)
            if len(ext) > 0 and ext[1:] in ALLOW_FILE_TYPE:
                file_type = ext[1:]
            else:  # 默认为 yaml；一般来说，如果是 json 文件，那么后缀大概率也是 json，但 yaml 则不一定（yaml 库也能加载 json）
                file_type = 'yaml'

    if file_type == 'json':
        cfg = _load_config_json(file_path)
    elif file_type == 'yaml':
        cfg = _load_config_yaml(file_path)
    else:
        raise ValueError('Error file_type: "%s"' % (file_type,))

    return cfg


def load_config(file_path=None, file_type=None):
    """
    配置文件加载装饰器
    
    Args:
        file_path: 
        file_type: 
        
    Examples:
        # 场景 1
        ```
        @load_config('_test/test_config.json')
        def main(cfg):
            """"""
            print(cfg)
        ```
        
        # 场景 2
        ```
        @load_config()
        def main(cfg):
            """"""
            print(cfg)
        
        > python xxx.py _test/test_config.yaml
        ```
    """

    def main_decorator(func):
        """"""

        @functools.wraps(func)
        def decorated_main():
            """"""
            cfg = _load_config_file(file_path, file_type)
            func(cfg)

        return decorated_main

    return main_decorator
