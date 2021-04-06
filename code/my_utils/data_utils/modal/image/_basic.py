#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-04-06 7:37 下午
    
Author:
    huayang
    
Subject:
    
"""
import os
import io

from PIL import Image


def get_real_ext(image_path, return_is_same=False):
    """
    获取图像文件的真实后缀
    如果不是图片，返回后缀为 None
    该方法不能判断图片是否完整

    Args:
        image_path:
        return_is_same: 是否返回 `is_same`

    Returns:
        ext_real, is_same
        真实后缀，真实后缀与当前后缀是否相同
        如果当前文件不是图片，则 ext_real 为 None
    """
    import imghdr

    # 获取当前后缀
    ext_cur = os.path.splitext(image_path)[1]

    if ext_cur.startswith('.'):
        ext_cur = ext_cur[1:]

    # 获取真实后缀
    ext_real = imghdr.what(image_path)

    if return_is_same:
        # 是否相同
        is_same = ext_cur == ext_real or {ext_cur, ext_real} == {'jpg', 'jpeg'}

        return ext_real, is_same

    return ext_real


def rename_to_real_ext(image_path):
    """将图片重命名为真实后缀"""
    ext_real, is_same = get_real_ext(image_path, return_is_same=True)

    if is_same or ext_real is None:
        return

    prefix, _ = os.path.splitext(image_path)
    dst = '.'.join([prefix, ext_real])
    os.rename(image_path, dst)


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