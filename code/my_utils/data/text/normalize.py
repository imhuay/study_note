#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Time:
    2021-04-23 3:04 下午
    
Author:
    huayang
    
Subject:
    
"""
import re
import unicodedata
import opencc


t2s = opencc.OpenCC('t2s.json')

# 一些特殊处理的全角到半角映射
FULL2HALF_SPECIAL = {
    '\u3000': ' ',  # 全角空格
    '。': '.',  # 中文句号
}

CN_PUNCTUATION = set('，。？！、；：“”‘’（）《》〈〉【】『』「」﹃﹄〔〕…—～·')
SP_PUNCTUATION = set('$+<=>^`|')
RE_WHITE_SPACE = re.compile(r'\s+', re.UNICODE)


def is_space(c):
    """是否空白符"""
    return c == ' ' or c == '\n' or c == '\r' or c == '\t' or unicodedata.category(c) == 'Zs'


def is_control(c):
    """是否控制符"""
    if c == '\t' or c == '\n' or c == '\r':  # 这些作为空白符
        return False
    return unicodedata.category(c) in ('Cc', 'Cf')


def is_punctuation(c):
    """是否标点，包括全角、半角，以 py3 为准"""
    return c in '$+<=>^`|' or unicodedata.category(c).startswith('P')


def is_chinese_punctuation(c):
    """"""
    return c in CN_PUNCTUATION


def is_half_char(c):
    """是否半角字符"""
    if isinstance(c, str):
        c = ord(c)
    return 0x0020 <= c <= 0x007E


def is_full_char(c):
    """是否全角字符"""
    return is_half_char(ord(c) - 0xFEE0) or c in FULL2HALF_SPECIAL


def is_full_alphabet(c):
    """是否全角字母"""
    if isinstance(c, str):
        c = ord(c)
    return (0xFF21 <= c <= 0xFF3A) or (0xFF41 <= c <= 0xFF5A)


def is_full_number(c):
    """是否全角数字"""
    if isinstance(c, str):
        c = ord(c)
    return 0xFF10 <= c <= 0xFF19


def is_chinese_char(c):
    """是否中文字符"""
    if isinstance(c, str):
        c = ord(c)
    return 0x4E00 <= c <= 0x9FFF


def is_cjk_char(c):
    """是否 cjk 字符"""
    # This defines a "chinese character" as anything in the CJK Unicode block:
    #   https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block)
    #
    # Note that the CJK Unicode block is NOT all Japanese and Korean characters,
    # despite its name. The modern Korean Hangul alphabet is a different block,
    # as is Japanese Hiragana and Katakana. Those alphabets are used to write
    # space-separated words, so they are not treated specially and handled
    # like the all of the other languages.
    if isinstance(c, str):
        c = ord(c)

    return ((0x4E00 <= c <= 0x9FFF) or
            (0x3400 <= c <= 0x4DBF) or
            (0x20000 <= c <= 0x2A6DF) or
            (0x2A700 <= c <= 0x2B73F) or
            (0x2B740 <= c <= 0x2B81F) or
            (0x2B820 <= c <= 0x2CEAF) or
            (0xF900 <= c <= 0xFAFF) or
            (0x2F800 <= c <= 0x2FA1F))


def full2half_width(c):
    """全角转半角"""
    if c in FULL2HALF_SPECIAL:
        return FULL2HALF_SPECIAL.get(c)
    else:
        i = ord(c) - 0xFEE0
        return chr(i) if is_half_char(i) else c  # 转完之后不是半角字符返回原来的字符


def strip_accent(seq, form='NFD'):
    """移除重音符号

    Args:
        seq(str):
        form(str): one of {'NFD', 'NFKD'}

    Examples:
        strip_accents('âčè')  # ace
    """
    seq = unicodedata.normalize(form, seq)
    ret = [c for c in seq if unicodedata.category(c) != 'Mn']
    return "".join(ret)


def normalize(seq: str, to_lower=True, to_half=True, to_simplified=True, remove_accent=True):
    """文本归一化

    Args:
        seq:
        to_lower: 默认转小写
        to_half: 默认转半角，但不包括中文标点
        to_simplified: 默认中文繁转简
        remove_accent: 默认移除重音符号，如 'âčè' -> 'ace'
    """
    if remove_accent:  # 移除重音
        seq = strip_accent(seq)

    if to_lower:  # 转小写
        seq = seq.lower()

    if to_simplified:
        seq = t2s.convert(seq)

    cs = []
    for c in seq:
        if is_control(c):  # 移除控制符
            continue
        elif is_space(c):  # 空白符转空格
            cs.append(' ')
        elif is_full_char(c) and not is_chinese_punctuation(c) and to_half:  # 全角转半角，但不包括中文标点
            cs.append(full2half_width(c))
        else:  # 保持不变
            cs.append(c)

    seq = ''.join(cs)
    seq = RE_WHITE_SPACE.sub(' ', seq)  # 连续空格合并
    return seq


if __name__ == '__main__':
    """"""
    txt = '電影《２０１２》講述了２０１２年１２月２１日的世界末日，主人公 \t Ｊâｃｋ以及世界各國人民挣扎求生的经历，灾难面前，尽现人间百态。'
    print(txt)
    nt = normalize(txt)
    print(nt)

