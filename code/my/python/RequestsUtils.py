#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-06-23 8:43 下午
    
Author:
    huayang
    
Subject:
    requests 相关函数：主要是请求网络，下载等
"""
import requests


def get_response(url,
                 timeout=3,
                 n_retry_max=5,
                 return_content=False,
                 check_func=None):
    """
    Args:
        url:
        timeout: 超时时间，单位秒
        n_retry_max: 最大重试次数
        return_content: 是否返回 response.content
        check_func: 内容检查函数，函数接收单个 response 对象作为参数
    """
    n_retry = 0
    response = None
    while n_retry < n_retry_max:
        try:
            response = requests.get(url=url, timeout=timeout)
            if return_content:
                response = response.content
            if check_func is None or check_func(response):
                break
        except:
            pass
        finally:
            n_retry += 1

    return response


def download_from_url(url,
                      save_path=None,
                      **kwargs):
    """
    下载指定 url 内容

    Args:
        url:
        save_path: 保存路径
        kwargs: get_response 相关参数

    """
    response = get_response(url, **kwargs)

    if response and save_path:
        with open(save_path, mode='wb') as f:
            f.write(response.content)

    return save_path


def _test_multi_download():
    """测试多线程下载"""
    from my.python.ThreadUtils import run_multi_thread

    args_ls = [('https://www.baidu.com/', './-out/baidu1.html'),
               ('https://www.baidu.com/', './-out/baidu2.html'),
               ('https://www.baidu.com/', './-out/baidu3.html')]

    ret = run_multi_thread(download_from_url, args_ls, star_args=True)
    print(ret)


if __name__ == '__main__':
    """"""
    _test_multi_download()