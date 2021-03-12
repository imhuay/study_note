#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-03-11 9:20 下午
    
Author:
    huayang
    
Subject:
    
"""

import tensorflow as tf

try:
    import tensorflow.keras as keras
    import tensorflow.keras.backend as K
except:
    import keras
    import keras.backend as K


def build_model(input_shape, base_layers, n_class, dropout_rate=0.2):

    inputs = keras.layers.Input(shape=input_shape)
    x = keras.layers.Dropout(dropout_rate)(inputs)

    if not isinstance(base_layers, list):
        base_layers = [base_layers]

    for base_layer in base_layers:
        x = keras.layers.TimeDistributed(base_layer)(x)
        x = keras.layers.Dropout(dropout_rate)(x)

    outputs = keras.layers.Dense(n_class, activation='softmax')(x)
    model = keras.Model(inputs, outputs)
    return model


