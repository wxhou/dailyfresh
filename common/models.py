#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_time = models.DateTimeField(_('create time'), auto_now_add=True, help_text='创建时间')
    updated_time = models.DateTimeField(_('update time'), auto_now=True, help_text="更新时间")
    status = models.SmallIntegerField(_('status'), default=0, help_text='状态')
    is_deleted = models.BooleanField(_('is deleted'), default=False, help_text='是否删除')

    class Meta:
        abstract = True
