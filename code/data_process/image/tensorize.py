#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-03-09 10:42
    
Author:
    huayang
    
Subject:
    图片张量化，提供了基于 PIL 和 cv2 的两种方法；
    一般建议使用 cv2，其操作即中间结果均基于 np.ndarray；
    而 PIL 会先将图片转为 Image 实例，再进行操作（API 更直观）

Note:
    基于 base64 的序列化方法详见：python_utils/basic_utils/serialize.py

    - 库版本
        - tensorflow >= 2.0

References:
    keras.preprocessing.image
"""
import io

import cv2
import numpy as np
from PIL import Image


class TensorizeByPIL(object):

    @staticmethod
    def load_image(src, color_mode='RGB'):
        """
        加载原始图像，返回 PIL.Image 对象

        Args:
            src(str or bytes): 图像路径，或二进制数据
            color_mode(str): 颜色模式，支持 {"L","RGB","RGBA"} 种类型，对应的 shape 分别为 (w, h)、(w, h, 3)、(w, h, 4)

        Returns: Image.Image
        """
        if color_mode not in {"I", "L", "RGB", "RGBA"}:
            raise ValueError('Unsupported color_mode: %s, it must be one of {"L", "RGB", "RGBA"}' % color_mode)

        if isinstance(src, bytes):
            img = Image.open(io.BytesIO(src))
        else:
            with open(src, 'rb') as f:
                img = Image.open(io.BytesIO(f.read()))

        if img.mode != color_mode:
            img = img.convert(color_mode)

        return img

    @staticmethod
    def image_to_tensor(img, resize=None, color_mode='RGB', dtype=np.uint8):
        """
        将 PIL.Image 对象转为 numpy 数组

        Args:
            img(str or bytes or Image.Image):
            resize:
            color_mode:
            dtype:

        Returns:

        """
        if isinstance(img, (str, bytes)):
            img = TensorizeByPIL.load_image(img, color_mode=color_mode)

        if resize:
            img = img.resize(size=resize)

        x = np.asarray(img, dtype=dtype)
        if len(x.shape) == 2:
            x = x.reshape((x.shape[0], x.shape[1], 1))

        return x

    @staticmethod
    def tensor_to_image(x, save_path=None, scale=False):
        """
        将 numpy 数组转为 PIL.Image 对象

        Args:
            x:
            save_path:
            scale:

        """
        x = np.asarray(x, np.float32)
        if x.ndim != 3:
            raise ValueError('Unsupported tensor dim: %s, it must be 3' % len(x.shape))

        if scale:
            x = x - np.min(x)
            x_max = np.max(x)
            if x_max != 0:
                x /= x_max
            x *= 255

        n_channel = x.shape[2]
        if n_channel == 3:
            color_mode = 'RGB'
        elif n_channel == 4:
            color_mode = 'RGBA'
        elif n_channel == 1:
            x = x[:, :, 0]
            if np.max(x) > 255:
                color_mode = 'I'
            else:
                color_mode = 'L'
        else:
            raise ValueError('Unsupported channel number: %s, it must be one of {1, 3, 4}' % n_channel)

        dtype = np.uint8
        if color_mode == 'I':
            dtype = np.int32

        img = Image.fromarray(x.astype(dtype), color_mode)

        if save_path:
            img.save(save_path)

        return img


class TensorizeByCV2(object):

    @staticmethod
    def image_to_tensor(img, resize=None, color_mode=cv2.IMREAD_COLOR):
        """"""
        if isinstance(img, str):
            with open(img, 'rb') as f:
                img = f.read()

        x = cv2.imdecode(np.frombuffer(img, dtype=np.uint8), flags=color_mode)

        if resize:
            x = cv2.resize(x, dsize=resize)

        return x

    @staticmethod
    def tensor_to_image(x, save_path, scale=False):
        """"""
        if scale:
            x = x - np.min(x)
            x_max = np.max(x)
            if x_max != 0:
                x /= x_max
            x *= 255

        cv2.imwrite(save_path, x)


Tensorize = TensorizeByCV2


def _test_TensorizeByPIL():
    """"""
    _obj = open('../_test_data/pok.jpg', 'rb').read()
    _img = TensorizeByPIL.load_image(_obj)
    print(isinstance(_img, Image.Image))

    _x = np.asarray(_img)
    print(np.max(_x))

    _x = TensorizeByPIL.image_to_tensor(_img, resize=(224, 224))
    print(_x.shape)
    print(_x.dtype)

    _save_path = '../_test_data/-out/pok.jpg'
    _img = TensorizeByPIL.tensor_to_image(_x, save_path=_save_path)
    print(isinstance(_img, Image.Image))


def _test_TensorizeByCV2():
    """"""
    _obj = open('../_test_data/pok.jpg', 'rb').read()
    _x = TensorizeByCV2.image_to_tensor(_obj, resize=(224, 224))
    print(_x.shape)
    print(_x.dtype)

    _save_path = '../_test_data/-out/pok.jpg'
    TensorizeByCV2.tensor_to_image(_x, _save_path)


if __name__ == '__main__':
    """"""
    # _test_TensorizeByPIL()
    _test_TensorizeByCV2()
