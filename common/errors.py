#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
errors.py
"""


class System(object):
    """
    System
    """
    ERROR = 1001
    ERROR_DETAIL = 1002
    DATE_FMT_ERROR = 1003
    NOT_FOUND = 1004
    FIELD_REQUIRED = 1005
    FMT_ERROR = 1006
    PARAMS_ERROR = 1007
    NOT_OWNER = 1008


class Account(object):
    """
    Account
    """
    MOBILE_FORMAT = 2001
    GET_CAPTCHA = 2002
    CAPTCHA_ERROR = 2003
    SIGNATURE = 2004
    CODE = 2005
    REFRESH_TOKEN = 2006
    UNAUTHORIZED = 2007
    MOBILE_REQUIRED = 2008
    REQUESTS_MULTI = 2009
    INVALID_CODE = 2010
    ENCRYPTED_DATA = 2011
    IV = 2012
    DECRYPTED_DATA = 2013
    AVATAR = 2014
    NICK_NAME = 2015
    USERNAME_OR_PASSWORD = 2016
    TOKEN = 2017
    USER_UN_CERTIFIED_ROOM = 2018
    USER_OR_PHONE_NOT_EXIST = 2019
    REGISTER_ERROR = 2020


class YUNPIAN(object):
    """
    YUNPIAN
    """
    BAD_RESPONSE = 3001


class VerifyCode(object):
    """
    VerifyCode
    """
    CODE_NOT_EXIST = 4000
    CODE_EXPIRED = 4001
    CODE_NOT_EQUAL = 4002
    CODE_IMG_NOT_EXIST = 4003
    CODE_SMS_NOT_EXIST = 4004
    CODE_IMG_NOT_EQUAL = 4005
    CODE_SMS_NOT_EQUAL = 4006
    TRY_AGAIN_ONE_MINUTE = 4007
    TRY_AGAIN_ONE_HOUR = 4008


class UploadFileCode(object):
    """
    UploadFileCode
    """
    FILE_IS_NONE = 5001


class QrCode(object):
    """
    QrCode
    """
    WIDTH_HEIGHT_NOT_EQUAL = 6001
