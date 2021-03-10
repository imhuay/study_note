#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-03-10 4:00 PM
    
Author:
    huayang
    
Subject:
    文件下载
"""
import os
import requests

from tqdm import tqdm


def download_once(url,
                  save_path=None,
                  save_mode='wb',
                  save_encoding=None,
                  timeout=3,
                  n_retry_max=5,
                  return_response=False,
                  check_func=None, **kwargs):
    """
    下载指定 url 内容

    Args:
        url:
        save_path: 保存路径
        save_mode: 保存模式，默认为 'wb'
        save_encoding: 保存文件编码，save_mode='w' 时，才需要修改
        timeout: 超时时间，单位秒
        n_retry_max: 最大重试次数
        return_response: 是否返回 response.content
        check_func: 内容检查函数
        kwargs: check_func 可能需要的额外参数

    """

    n_retry = 0
    response = None
    while n_retry < n_retry_max:
        try:
            response = requests.get(url=url, timeout=timeout).content
            if check_func is None or check_func(response, **kwargs):
                break
        except:
            pass
        finally:
            n_retry += 1

    if response and save_path:
        with open(save_path, mode=save_mode, encoding=save_encoding) as f:
            f.write(response)

    if return_response:
        return response


def download_multi_thread(save_dir, download_func, arg_ls, n_thread=None, use_iter=True):
    """
    多线程下载

    Args:
        save_dir: 保存路径（文件夹）
        download_func: 下载函数
        arg_ls: 参数列表
        n_thread: 线程数
        use_iter: 是否使用迭代器模式，默认为 False，即使用生成器模式，为 True 时使用迭代器模式
            显式区别在于 tqdm ：
                生成器为 2it [00:00, 16.88it/s]，
                迭代器为 100%|██████████| 2/2 [00:00<00:00, 16.88it/s]
            一般建议都使用生成器模式，但是文件数量较少时可以考虑使用迭代器模式（可以了解下载进度）

    """
    from multiprocessing.pool import ThreadPool

    os.makedirs(save_dir, exist_ok=True)

    ret_ls = []
    with ThreadPool(n_thread) as p:
        ret_iter = p.imap_unordered(lambda args: download_func(*args), arg_ls)

        if use_iter:
            ret_iter = list(ret_iter)

        for it in tqdm(ret_iter):
            ret_ls.append(it)

    return ret_ls


if __name__ == '__main__':
    """"""
    args = [
        ('https://www.baidu.com/', './_out/baidu1.html'),
        ('https://www.baidu.com/', './_out/baidu2.html'),
        ('https://www.baidu.com/', './_out/baidu3.html'),
    ]

    download_multi_thread('./_out', download_once, args)
