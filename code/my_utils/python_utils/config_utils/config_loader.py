#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-04-01 7:23 下午
    
Author:
    huayang
    
Subject:
    一个用于加载配置文件的装饰器，偷师于 facebook 的开源库 hydra

Examples:
    ```
    @load_config('./test_config.json')
    def main(cfg):
        """"""
        print(type(cfg))
        print(cfg)
    ```

References:
    facebookresearch/hydra | https://github.com/facebookresearch/hydra
"""
import json
import functools

from .bunch import Bunch


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


def load_config(path, file_type='json'):
    """"""

    def main_decorator(func):
        """"""

        @functools.wraps(func)
        def decorated_main():
            """"""
            if file_type == 'json':
                cfg = _load_config_json(path)
            elif file_type == 'yaml':
                cfg = _load_config_yaml(path)
            else:
                raise ValueError('Error file_type')

            func(cfg)

        return decorated_main

    return main_decorator
