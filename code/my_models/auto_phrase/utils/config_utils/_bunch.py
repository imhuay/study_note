#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-03-15 6:03 下午
    
Author:
    huayang
    
Subject:
    利用 dict 实现简单的 Bunch 模式
"""


class Bunch(dict):
    """
    Examples:

        >>> b = Bunch(a=1, b=2)
        >>> b['a']
        1
        >>> b.b
        2
        >>> b.c = 3
        >>> b.c
        3
        >>> d = Bunch(d=4, e=b)
        >>> d
        {'d': 4, 'e': {'a': 1, 'b': 2, 'c': 3}}

    """

    def __init__(self, *args, **kwargs):
        super(Bunch, self).__init__(*args, **kwargs)

    def __setattr__(self, key, value):
        self[key] = value

    def __dir__(self):
        return self.keys()

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __delattr__(self, k):
        try:
            del self[k]
        except KeyError:
            raise AttributeError(k)

    @staticmethod
    def from_dict(d):
        return _bunch(d)

    def to_dict(self):
        return _unbunch(self)


def _bunch(x):
    """ Recursively transforms a dictionary into a Bunch via copy.

        >>> b = _bunch({'urmom': {'sez': {'what': 'what'}}})
        >>> b.urmom.sez.what
        'what'

        bunchify can handle intermediary dicts, lists and tuples (as well as
        their subclasses), but ymmv on custom datatypes.

        >>> b = _bunch({ 'lol': ('cats', {'hah':'i win again'}),
        ...         'hello': [{'french':'salut', 'german':'hallo'}] })
        >>> b.hello[0].french
        'salut'
        >>> b.lol[1].hah
        'i win again'

        nb. As dicts are not hashable, they cannot be nested in sets/frozensets.
    """
    if isinstance(x, dict):
        return Bunch((k, _bunch(v)) for k, v in x.items())
    elif isinstance(x, (list, tuple)):
        return type(x)(_bunch(v) for v in x)
    else:
        return x


def _unbunch(x):
    """ Recursively converts a Bunch into a dictionary.

        >>> b = Bunch(foo=Bunch(lol=True), hello=42, ponies='are pretty!')
        >>> _unbunch(b)
        {'foo': {'lol': True}, 'hello': 42, 'ponies': 'are pretty!'}

        unbunchify will handle intermediary dicts, lists and tuples (as well as
        their subclasses), but ymmv on custom datatypes.

        >>> b = Bunch(foo=['bar', Bunch(lol=True)], hello=42,
        ...         ponies=('are pretty!', Bunch(lies='are trouble!')))
        >>> _unbunch(b) #doctest: +NORMALIZE_WHITESPACE
        {'foo': ['bar', {'lol': True}], 'hello': 42, 'ponies': ('are pretty!', {'lies': 'are trouble!'})}

        nb. As dicts are not hashable, they cannot be nested in sets/frozensets.
    """
    if isinstance(x, dict):
        return dict((k, _unbunch(v)) for k, v in x.items())
    elif isinstance(x, (list, tuple)):
        return type(x)(_unbunch(v) for v in x)
    else:
        return x


def _test():
    b = Bunch(foo=Bunch(lol=True), hello=42, ponies='are pretty!')
    print(b)

    del b.hello
    print('hello' in b)  # False

    d = {'a': 1, 'b': 2, 'c': {'aa': 11, 'bb': 22}}
    b = Bunch.from_dict(d)
    print(b.c.aa)


if __name__ == '__main__':
    """"""
    _test()
