#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging
import requests
from random import choice

logger = logging.getLogger('debug')


class YunPian(object):

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    @staticmethod
    def generate_code():
        """
        生成四位数验证码
        :return:
        """
        seeds = '1234567890'
        return "".join([choice(seeds) for _ in range(4)])

    def send_sms(self, code, mobile):
        if self.api_key is None:
            logger.debug('\n\n【每日新鲜】你的验证码为：{}\n\n'.format(code))
            return {'errcode': 0, 'errmsg': "短信发送成功"}
        data = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【每日新鲜】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }
        headers = {
            "Accept": "application/json;charset=utf-8;",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8;"
        }
        response = requests.post(self.single_send_url, data=data, headers=headers)
        return response.json()


if __name__ == "__main__":
    yun_pian = YunPian()
    yun_pian.send_sms("2017", "18291900215")
