#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-03-09 10:42
    
Author:
    huayang
    
Subject:
    图片张量化，提供了基于 PIL、cv2、tf 的三种方法；
    三种方法获取的张量会存在差异（但是应该没问题，使用它们重新另存的图片未改变，模型不至于处理不了这种程度的泛化）

Note:
    - 基于 base64 的序列化方法可以参考：python_utils/basic_utils/serialize.py
    - 使用 tf 版本需要 tensorflow >= 2.0，因为用到了 x.numpy()
    - cv2 读取的图片默认通道顺序为 bgr，这个需要注意：
        - 如果要把 cv2 读取的图片用其他库处理，则需要先调整为 rgb；反之其他库处理的图片传给 cv2，需要先转回 bgr；
        - 换言之，尽量使用同一套库，要么都用 cv2 处理，要么都不用；

References:
    keras.preprocessing.image
"""
import io

import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from PIL import Image


def tensor_to_image(x, save_path=None, scale=False):
    """
    将 numpy 数组转为 PIL.Image 对象

    Args:
        x:
        save_path:
        scale:

    """
    x = np.asarray(x, np.float32)

    if scale:
        x = x - np.min(x)
        x_max = np.max(x)
        if x_max != 0:
            x = x / x_max
        x *= 255

    if x.ndim == 3:
        n_channel = x.shape[2]
        if n_channel == 3:
            color_mode = 'RGB'
        elif n_channel == 4:
            color_mode = 'RGBA'
        elif n_channel == 1:
            x = x[:, :, 0]
            color_mode = 'I' if np.max(x) > 255 else 'L'
        else:
            raise ValueError('Unsupported channel number: %s, it must be one of {1, 3, 4}' % n_channel)
    elif x.ndim == 2:
        color_mode = 'I' if np.max(x) > 255 else 'L'
    else:
        raise ValueError('Unsupported tensor dim: %s, it must be one of {2, 3}' % x.ndim)

    dtype = np.int32 if color_mode == 'I' else np.uint8
    img = Image.fromarray(x.astype(dtype), color_mode)

    if save_path:
        img.save(save_path)

    return img


class Tensorize(object):
    @staticmethod
    def load_image(src, color_mode='RGB') -> Image.Image:
        """
        加载原始图像，返回 PIL.Image 对象

        Args:
            src(str or bytes): 图像路径，或二进制数据
            color_mode(str): 颜色模式，支持 {"L","RGB","RGBA"} 种类型，对应的 shape 分别为 (w, h)、(w, h, 3)、(w, h, 4)

        Returns: Image.Image
        """
        if isinstance(src, bytes):
            img = Image.open(io.BytesIO(src))
        else:
            with open(src, 'rb') as f:
                img = Image.open(io.BytesIO(f.read()))

        if color_mode not in {"L", "RGB", "RGBA"}:
            raise ValueError('Unsupported color_mode: %s, it must be one of {"L", "RGB", "RGBA"}' % color_mode)

        if img.mode != color_mode:
            try:
                img = img.convert(color_mode)
            except:
                print('The color mode=%s can not convert to %s' % (img.mode, color_mode))

        return img

    @staticmethod
    def by_pil(img, resize=None, color_mode='RGB', dtype=np.uint8):
        """
        将 PIL.Image 对象转为 numpy 数组

        Args:
            img(str or bytes or Image.Image):
            resize:
            color_mode: 只支持 {"L","RGB","RGBA"}，如果是其他更专业的模式，参考 plt.imread、plt.pil_to_array 等的实现
            dtype:

        Returns:

        """
        if isinstance(img, (str, bytes)):
            img = Tensorize.load_image(img, color_mode=color_mode)

        if resize:
            img = img.resize(size=resize)

        x = np.asarray(img, dtype=dtype)
        if len(x.shape) == 2:
            x = x.reshape((x.shape[0], x.shape[1], 1))

        return x

    @staticmethod
    def by_cv2(img, resize=None, color_mode=cv2.IMREAD_COLOR, convert_to_rgb=True):
        """
        Args:
            img:
            resize:
            color_mode: 默认 cv2.IMREAD_COLOR
            convert_to_rgb: 是否将通道顺序转为 'RGB'，cv2 默认的通道顺序为 'BGR'

        """
        if isinstance(img, str):
            with open(img, 'rb') as f:
                img = f.read()

        x = cv2.imdecode(np.frombuffer(img, dtype=np.uint8), flags=color_mode)

        if resize:
            x = cv2.resize(x, dsize=resize)

        if convert_to_rgb:
            x = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)

        return x

    @staticmethod
    def by_tf(img, resize=None, return_numpy=False, expand_animations=False):
        """
        Args:
            img:
            resize:
            return_numpy:
            expand_animations: 默认 False，即 gif 只取第一帧
        """
        if isinstance(img, str):
            with open(img, 'rb') as f:
                img = f.read()

        x = tf.io.decode_image(img, channels=3, expand_animations=expand_animations)

        if resize:
            x = tf.image.resize(x, size=resize)

        if return_numpy:
            x = x.numpy()

        return x

    @staticmethod
    def by_plt(img):
        """
        内部其实是使用的 PIL.Image

        Args:
            img:

        Returns:

        """
        x = plt.imread(img)
        return x


def _test():
    """"""
    src = '../_test_data/pok.jpg'
    # src = open(src, 'br').read()

    x1 = Tensorize.by_pil(src, resize=(224, 224), color_mode='L')
    tensor_to_image(x1, '../_test_data/-out/pok_pil.jpg')
    x2 = Tensorize.by_cv2(src)
    print(x2.shape)
    tensor_to_image(x2, '../_test_data/-out/pok_cv2.jpg')
    # print((x1 == x2).all())  # False

    x3 = Tensorize.by_tf(src, return_numpy=True)
    # print((x1 == x3).all())  # False
    # print((x2 == x3).all())  # False
    tensor_to_image(x3, '../_test_data/-out/pok_tf.jpg')


def _test_save():
    src = '../_test_data/pok.jpg'
    img = Tensorize.load_image(src, 'RGB')
    img = img.convert('L')
    # plt.imshow(img)
    # plt.show()

    tensor_to_image(img, '../_test_data/-out/pok_L.jpg')


if __name__ == '__main__':
    """"""
    # _test()
    _test_save()
