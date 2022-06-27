#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import time
import datetime
import pytz
from django.utils import timezone


def get_now_tz(tz=pytz.UTC):
    """
    返回UTC时间
    :param tz:
    :return:
    """
    return datetime.datetime.now(tz=tz)


def local_time():
    """返回现在Unix时间"""
    return time.time()


def timestamp(length=13):
    """
    13时间戳
    :param length:
        求个位数: 1、(length / 1) % 10
                2、(a,b) = divmod(length, 10)  b是个位数
    :return:
    """
    return int(round(local_time() * (length / 1 % 10)))


def timedelta_from_future(*args, **kwargs):
    """
    时间差
        获取未来距离今天现在的某一天
    :param args:
    :param kwargs:
    :return:
    """
    return timezone.now() + datetime.timedelta(*args, **kwargs)


def timedelta_from_now(*args, **kwargs):
    """
    时间差
        获取过去距离今天的某一天
    """
    return timezone.now() - datetime.timedelta(*args, **kwargs)


def fmt_time(naive_time):
    """
    datetime.datetime.strftime
    格式化时间
    :param naive_time:
    :return:
    """
    fmt = '%Y-%m-%d %H:%M:%S'
    return naive_time.strftime(fmt)


if __name__ == '__main__':
    t = timedelta_from_now(7)
    print(t)
