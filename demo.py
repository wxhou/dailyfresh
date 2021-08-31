#!/usr/bin/env python3
# -*- coding:utf-8 -*-


def main(string):
    # 将str转成ascii码
    asc_list = [int(ord(c)) for c in string]
    # str1
    str_pool = "qwenaskjdhkjrhtjbjdbnasbdadoeewrwerukdfsdert"
    # 找到对应的字符
    res = []
    for i in asc_list:
        if chr(i) in str_pool:
            res.append(chr(i))
    # 拼接成新的字符串
    return "".join(res)


if __name__ == '__main__':
    raw_str = '3832_quanfangtong_1'
    print(main(raw_str))
