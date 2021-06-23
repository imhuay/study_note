#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-06-22 5:45 下午
    
Author:
    huayang
    
Subject:
    多线程相关
"""
from tqdm import tqdm
from multiprocessing.pool import ThreadPool


def run_multi_thread(func, args_iter, n_thread=None, ordered=False, use_imap=False, star_args=False):
    """
    Args:
        func: 回调函数
        args_iter: 参数序列
        n_thread: 线程数，默认 None
        ordered: 是否有序，默认 False；
            经测试即使为 False 也是有序的，可能与具体解释器有关；
        use_imap: 是否使用 imap，默认 False；
            使用 imap 可以利用 tqdm 估算进度，但是速度比 map 慢；
        star_args: 是否需要展开参数，默认 False，即默认 func 只接受一个参数；
            如果 func 形如 func(a, b, c)，则需要展开，而 func([a, b, c]) 则不需要；

    Returns:
        func(args) 的结果集合
    """
    if star_args:
        _func = lambda a: func(*a)
    else:
        _func = func

    ret = []
    with ThreadPool(n_thread) as p:
        if use_imap:
            map_func = p.imap_unordered
        else:
            map_func = p.map

        if ordered:
            _func_new = lambda a: (a[0], _func(a[1]))
            args_ls_new = [(i, args) for i, args in enumerate(args_iter)]
            ret_iter = map_func(_func_new, args_ls_new)
        else:
            ret_iter = map_func(_func, args_iter)

        if use_imap:
            ret_iter = tqdm(ret_iter)

        for it in ret_iter:
            ret.append(it)

    if ordered:
        ret = [it[1] for it in sorted(ret, key=lambda x: x[0])]

    return ret


def _test_star_args():
    """ star_args 参数测试 """

    def some_func(s, x):
        """一个简单的测试函数，输入 s 加一个后缀"""
        # time.sleep(math.sqrt(int(s)))
        return s + '-' + x

    # 构造参数序列
    args_ls = list([(str(i), str(i+1)) for i in range(1000)])
    ret1 = run_multi_thread(some_func, args_ls, star_args=True, ordered=True)
    print(ret1)

    def ss_func(a):  # 包成一个参数
        s, x = a
        return some_func(s, x)

    ret2 = run_multi_thread(ss_func, args_ls, star_args=False)
    # print(ret2)
    assert ret1 == ret2


def _test_download():
    """"""
    import os
    import requests

    ALLOW_FORMATS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

    def file_download(url, dir_path, file_name, timeout=3, n_retry_max=5):
        """数据下载"""

        def _get_ext(url: str):
            for ext in ALLOW_FORMATS:
                if -1 != url.find(ext):
                    return ext

            return '.jpg'

        n_retry = 0
        response = None
        while n_retry < n_retry_max:
            try:
                response = requests.get(url=url, timeout=timeout)
                break
            except:
                pass
            finally:
                n_retry += 1

        ext = _get_ext(url)
        save_path = os.path.join(dir_path, file_name + ext)

        if response:
            with open(save_path, 'wb') as fw:
                fw.write(response.content)

        return save_path

    def get_args_iter():

        main_path = '-out/test'
        url_ls = ['https://p0.meituan.net/dpmerchantpic/543d27fe7f877ea881c61ec859c6ddaa63445.jpg'] * 6
        label_ls = ['a', 'b', 'c'] * 2
        name_ls = ['a', 'b', 'c', 'd', 'e', 'f']

        os.makedirs(main_path, exist_ok=True)

        if label_ls is None:
            label_ls = [''] * len(url_ls)
        else:
            assert len(url_ls) == len(label_ls)
            label_st = set(label_ls)
            for label in label_st:
                os.makedirs(os.path.join(main_path, label), exist_ok=True)

        if name_ls is None:
            name_ls = list(str(i) for i in range(1, len(url_ls) + 1))

        args = [(url, os.path.join(main_path, label), file_name)
                for file_name, url, label in zip(name_ls, url_ls, label_ls)]

        return args

    args_ls = get_args_iter()
    ret = run_multi_thread(file_download, args_ls, star_args=True)
    print(ret)


if __name__ == '__main__':
    """"""
    _test_star_args()
    _test_download()
