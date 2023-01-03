#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from rest_framework import serializers

serializers.DateTimeField()


class PageSerializer(serializers.BaseSerializer):
    """
    Page Serializer
    """
    page = serializers.IntegerField(min_value=1, default=1, help_text='第几页')
    page_size = serializers.IntegerField(min_value=1, default=10, help_text="每页数量")
