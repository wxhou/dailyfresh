#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging
from datetime import timedelta
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils.timezone import now
from django.core.validators import FileExtensionValidator
from rest_framework import serializers, validators
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from .models import User, UserFav, UserAddress, UserLeavingMessage
from apps.goods.serializers import GoodsDetailSerializer

logger = logging.getLogger('debug')


class LoginSerializer(serializers.Serializer):
    """登录"""
    password = serializers.CharField(style={'input_type': 'password'}, help_text='密码',
                                     required=True, write_only=True,
                                     min_length=8, max_length=16)
    email = serializers.EmailField(required=True, help_text='注册邮箱', max_length=128)


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详情"""

    class Meta:
        model = User
        fields = ("id", "username", "name", "gender", "birthday", "email", "mobile", "avatar")

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserAvatarSerializer(serializers.Serializer):
    avatar = serializers.FileField(required=True, help_text="上传头像",
                                   validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])])


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
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate(self, attrs):
        logger.debug("register user: {}".format(attrs))
        return attrs

    class Meta:
        model = User
        fields = ('username', 'password', 'email', "mobile")


class UserFavDetailSerializer(serializers.ModelSerializer):
    """用户收藏详情"""
    goods = GoodsDetailSerializer(many=True)

    class Meta:
        model = UserFav
        fields = ('goods', 'id')


class UserFavSerializer(serializers.ModelSerializer):
    """用户收藏"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserFav
        validators = [
            validators.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('user', 'goods'),
                message='商品已收藏'
            )
        ]
        fields = ('user', 'goods', 'id')


class UserMessageSerializer(serializers.ModelSerializer):
    """用户留言管理"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    file = serializers.FileField(required=False, help_text="上传文件",
                                 validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'mp4'])])

    class Meta:
        model = UserLeavingMessage
        exclude = ('is_deleted', 'status')


class UserAddressSerializer(serializers.ModelSerializer):
    """用户地址管理"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserAddress
        exclude = ('is_deleted', 'status')
