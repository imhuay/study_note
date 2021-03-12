#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-03-11 9:20 下午
    
Author:
    huayang
    
Subject:
    使用全连接的视频分类模型
"""

import tensorflow as tf

try:
    import tensorflow.keras as keras
    import tensorflow.keras.backend as K
except:
    import keras
    import keras.backend as K


def build_model(input_shape, units, n_class, acts='relu', dropout_rate=0.2):
    """"""
    inputs = keras.layers.Input(shape=input_shape)
    x = keras.layers.Dropout(dropout_rate)(inputs)
    x = keras.layers.Flatten()(x)

    if not isinstance(units, list):
        units = [units]

    if not isinstance(acts, list):
        acts = [acts] * len(units)

    if len(units) != len(acts):
        raise ValueError('len(units_ls)=%s != len(act_ls)=%s' % (len(units), len(acts)))

    for n_unit, act in zip(units, acts):
        x = keras.layers.Dense(n_unit, activation=act)(x)

    outputs = keras.layers.Dense(n_class, activation='softmax')(x)
    model = keras.Model(inputs, outputs)
    return model
