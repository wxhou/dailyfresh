#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
choices.py
"""

"""
user
"""
SEX = (
    ("male", u"男"),
    ("female", "女")
)

MESSAGE_CHOICES = (
    (1, "留言"),
    (2, "投诉"),
    (3, "询问"),
    (4, "售后"),
    (5, "求购")
)
"""
goods
"""
CATEGORY_TYPE = (
    (1, "一级类目"),
    (2, "二级类目"),
    (3, "三级类目"),
)

"""
shop
"""
ORDER_STATUS = (
    ("TRADE_SUCCESS", "成功"),
    ("TRADE_CLOSED", "超时关闭"),
    ("WAIT_BUYER_PAY", "交易创建"),
    ("TRADE_FINISHED", "交易结束"),
    ("paying", "待支付"),
)
