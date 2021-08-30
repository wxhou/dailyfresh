#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
import requests


class YunPian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
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
        re_dict = json.load(response.text)
        return re_dict


if __name__ == "__main__":
    yun_pian = YunPian("")
    yun_pian.send_sms("2017", "")
