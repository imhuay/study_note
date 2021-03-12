#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-03-11 10:44 上午
    
Author:
    huayang
    
Subject:
    
"""
import os
import cv2
import numpy as np


def video_to_tensor(video_path, n_frame=None, n_step=None, resize=None, return_array=True):
    """
    视频转张量

    Args:
        video_path: 视频路径
        n_frame: 按固定帧数抽帧
        n_step: 按固定间隔抽帧
        resize: 调整图像大小，格式为 (w, h)
        return_array: 是否转化为 np.array，默认为 list of 每一帧的 np.array

    """
    if n_frame and n_step:
        raise ValueError('不能同时设置 n_frame 和 n_step.')

    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frames = []
    for _ in range(fps):
        ret, frame = cap.read()
        if ret:
            frames.append(frame)

    if n_frame:
        n_step = len(frames) // n_frame + 1 if len(frames) % n_frame != 0 else len(frames) // n_frame

    if n_step:
        frames = frames[::n_step] if n_step > 0 else frames

    if resize:
        frames = [cv2.resize(f, resize) for f in frames]

    if return_array:
        frames = np.stack(frames)

    return frames
