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


class CategoryCreateSerializer(serializers.ModelSerializer):
    """添加新的目录"""
    parent_category_id = serializers.IntegerField(required=False, write_only=True, help_text="父类目ID")

    class Meta:
        model = GoodsCategory
        fields = ("id", "name", "code", "desc", 'category_type', 'parent_category_id', 'navigation')


class GoodsImageSerializer(serializers.ModelSerializer):
    """商品图片"""

    class Meta:
        model = GoodsImage
        fields = ("image",)


class GoodsSerializer(serializers.ModelSerializer):
    """商品"""
    category = CategoryDetailSerializer(read_only=True)
    category_id = serializers.IntegerField(required=True, write_only=True)
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"


class HotWordSerializer(serializers.ModelSerializer):
    """热搜"""

    class Meta:
        model = HotSearchWords
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    """banner"""

    class Meta:
        model = Banner
        fields = "__all__"


class GoodsCategoryBanner(serializers.ModelSerializer):
    """商品轮播"""

    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"


class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BannerSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = CategoryDetailSerializer(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_brands(self):
        pass

    def get_ad_goods(self):
        pass
