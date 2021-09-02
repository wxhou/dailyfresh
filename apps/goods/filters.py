#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import django_filters
from django.db.models import Q
from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    pass