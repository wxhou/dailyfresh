#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from apps.goods.models import (Goods, GoodsImage, GoodsCategory, GoodsCategoryBrand,
                               HotSearchWords, Banner, IndexAd)

logger = logging.getLogger('debug')


class CategoryDetailSerializer(serializers.ModelSerializer):
    """商品种类详情"""
    sub_cat = RecursiveField(allow_null=True, many=True, required=False)

    class Meta:
        model = GoodsCategory
        fields = ("id", "name", "code", "desc", 'category_type', 'sub_cat', 'navigation')


class GoodsImageSerializer(serializers.ModelSerializer):
    """商品图片"""

    id = serializers.IntegerField(required=True)
    image = serializers.ImageField(required=True, max_length=512, allow_empty_file=False, help_text='商品图片')

    class Meta:
        model = GoodsImage
        fields = ("id", "image")


class GoodsDetailSerializer(serializers.ModelSerializer):
    """商品详情"""
    category = CategoryDetailSerializer(read_only=True)
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        exclude = ('is_deleted', 'status')


class HotWordSerializer(serializers.ModelSerializer):
    """热搜词列表"""

    class Meta:
        model = HotSearchWords
        exclude = ('is_deleted', 'status')


class BannerSerializer(serializers.ModelSerializer):
    """banner"""

    class Meta:
        model = Banner
        exclude = ('is_deleted', 'status')


class GoodsCategoryBanner(serializers.ModelSerializer):
    """商品轮播"""

    class Meta:
        model = GoodsCategoryBrand
        exclude = ('is_deleted', 'status')


class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BannerSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = CategoryDetailSerializer(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_brands(self):
        pass

    def get_ad_goods(self):
        pass
