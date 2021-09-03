#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from apps.user.models import User


class CustomBackend(ModelBackend):
    """
    验证函数
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.filter(email=username, is_active=True).first()
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
