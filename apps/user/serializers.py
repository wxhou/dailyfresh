#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging
import datetime
from django.conf import settings
from rest_framework import serializers, validators
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from common.validators import PhoneValidator
from .models import User, VerifyCode

logger = logging.getLogger('debug')


class SmsSerializer(serializers.Serializer):
    """验证码"""
    mobile = serializers.CharField(max_length=11,
                                   validators=[PhoneValidator,
                                               validators.UniqueValidator(User.objects.all())])


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详情"""

    class Meta:
        model = User
        fields = ("name", "gender", "birthday", "email", "mobile")


class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册"""
    # code = serializers.CharField(required=True, write_only=True, max_length=4, min_length=4, label="验证码",
    #                              error_messages={
    #                                  "blank": "请输入验证码",
    #                                  "required": "请输入验证码",
    #                                  "max_length": "验证码格式错误",
    #                                  "min_length": "验证码格式错误"
    #                              },
    #                              help_text="验证码")
    username = serializers.CharField(label='用户名', required=True, help_text='用户名',
                                     validators=[validators.UniqueValidator(User.objects.all(), message="用户已存在")])

    password = serializers.CharField(style={'input_type': 'password'}, help_text='密码', required=True, write_only=True,
                                     min_length=8, max_length=16
                                     )
    email = serializers.EmailField(required=True, help_text='注册邮箱', max_length=128,
                                   validators=[validators.UniqueValidator(User.objects.all())])

    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()

    def validate(self, attrs):
        logger.debug("register user: {}".format(attrs))
        # v_code = VerifyCode.objects.filter(mobile=attrs['username']).last()
        # if not v_code:
        #     raise ValidationError("验证码错误")
        # end_time = datetime.datetime.now() - datetime.timedelta(minutes=settings.REGISTER_CONFIRM_TIMEDELTA)
        # if end_time > v_code.created_time:
        #     raise ValidationError("验证码已过期")
        # attrs['mobile'] = attrs['username']
        return attrs

    class Meta:
        model = User
        fields = ('username', 'mobile', 'password', 'email')
