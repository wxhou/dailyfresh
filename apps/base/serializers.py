#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging
from rest_framework import serializers

logger = logging.getLogger('debug')


class UploadSerializer(serializers.Serializer):
    file = serializers.FileField(help_text='上传文件')
    uniqueId = serializers.CharField(help_text='MD5')



