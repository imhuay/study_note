#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-03-11 11:38 上午
    
Author:
    huayang
    
Subject:
    1. 将视频转换成 tensor，形式上每个视频的 shape 为 [n, w, h, c]，其中 n 为视频帧数，后三维同图像
    2. 将每个视频的原始 tensor 传入预训练模型，获取特征
        这种方式相当于默认该图像预训练模型不参与训练，只是提供每一帧的特征
        一个视频的原始 tensor 可以看做一个 batch 的原始图像 tensor，因此可以直接传入一般的图像预训练模型，以 Xception 为例
        video_tensor = ...  # [n, w, h, c]
        feature = Xception.predict(video_tensor)  # [n, w', h', f]
        视情况决定是否再接一个 GlobalPooling 层，得到 shape=[n, f] 的特征
    3. 下面的过程跟一般分类模型类似

"""
import os
import argparse

import numpy as np
import tensorflow as tf

try:
    import tensorflow.keras as keras
    import tensorflow.keras.backend as K
except:
    import keras
    import keras.backend as K

from utils.tensorize import video_to_tensor


def get_args():
    """参数准备"""
    p = argparse.ArgumentParser()
    args = p.parse_args()

    # args = Bunch()

    file_path_ls = []
    label_ls = []
    # 赋值相关参数
    args.file_path_ls = file_path_ls
    args.label_ls = label_ls
    args.n_frame = 10
    args.n_feature = 2048  # 视预训练模型而定
    args.n_class = 8
    args.n_epoch = 10
    args.target_shape = (args.n_frame, args.n_feature)
    args.weights_file = r'../model_file/xception/xception_weights_tf_dim_ordering_tf_kernels_notop.h5'

    return args


def get_video_tensor(file_path_ls, n_frame=None):
    """"""
    video_tensor_ls = []
    for fp in file_path_ls:
        t = video_to_tensor(fp, n_frame=n_frame)
        video_tensor_ls.append(t)

    return video_tensor_ls


def get_feature_extractor(weights_file):
    """"""
    from tensorflow.keras.applications import Xception
    xception = Xception(include_top=False, weights=weights_file)
    outputs = keras.layers.GlobalAveragePooling2D(name="avg_pool")(xception.output)
    model = keras.Model(xception.input, outputs)
    return model


def get_video_feature(feature_extractor: keras.Model, file_path_ls, label_ls, n_frame, target_shape):
    """"""
    assert len(file_path_ls) == len(label_ls)

    feature_ls = []
    new_label_ls = []
    for fp, label in zip(file_path_ls, label_ls):
        vt = video_to_tensor(fp, n_frame=n_frame)
        fe = feature_extractor.predict(vt)

        if fe.shape != target_shape:
            continue

        new_label_ls.append(label)
        feature_ls.append(fe)

    return feature_ls, new_label_ls


def get_dataset(feature_ls, label_ls, batch_size=8):
    """"""
    ds_train = tf.data.Dataset.from_tensor_slices((feature_ls, label_ls))
    ds_train.shuffle(batch_size * 10)
    ds_train.batch(batch_size)

    return ds_train


def build_model(args):
    """"""
    inputs = keras.layers.Input(shape=(args.n_frame, args.n_feature))
    x = keras.layers.Flatten()(inputs)
    x = keras.layers.Dense(units=1024, activation='relu')(x)
    outputs = keras.layers.Dense(units=args.n_class, activation='softmax')(x)
    model = keras.Model(inputs, outputs)

    model.compile(optimizer='sgd', loss="binary_crossentropy", metrics=['accuracy'])
    return model


def main():
    """"""
    args = get_args()

    if not os.path.exists(args.inputs_save_path):
        feature_extractor = get_feature_extractor(args.weights_file)
        feature_ls, label_ls = get_video_feature(feature_extractor,
                                                 args.file_path_ls,
                                                 args.label_ls,
                                                 args.n_frame,
                                                 args.target_shape)
        # 保存
        np.savez(args.inputs_save_path, features=feature_ls, labels=label_ls)
    else:
        tmp = np.load(args.inputs_save_path)
        feature_ls = tmp['features']
        label_ls = tmp['labels']

    ds_train = get_dataset(feature_ls, label_ls)

    model = build_model(args)
    model.fit(ds_train, epochs=args.n_epoch)


def _test():
    """"""
    videl_path = r'/Users/huayang/workspace/my/study_note/code/data_process/_test_data/v_ApplyEyeMakeup_g01_c01.avi'
    t = video_to_tensor(videl_path, n_frame=10)
    print(t.shape)

    weights_file = r'../model_file/xception/xception_weights_tf_dim_ordering_tf_kernels_notop.h5'
    model = get_feature_extractor(weights_file)
    f = model.predict(t)
    print(f.shape)


if __name__ == '__main__':
    """"""
    _test()
