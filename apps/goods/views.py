from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from apps.goods.models import Goods, GoodsCategory
from .serializers import CategoryDetailSerializer, CategoryCreateSerializer, GoodsSerializer


# Create your views here.

class GoodsCategoryViewSet(viewsets.ModelViewSet):
    """商品分类管理
    list:
        获取商品分类列表

        ---

    retrieve:
        获取商品分类详情

        ---

    create:
        添加商品分类

        ---

    destroy:
        删除一个商品分类

        ---

    update:
        更新一个商品分类

        ---

    partial:
        局部更新一个商品分类

        ---

    """
    queryset = GoodsCategory.objects.filter(category_type=1, is_deleted=False, status=0)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return CategoryDetailSerializer
        return CategoryCreateSerializer

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


class GoodsViewSet(viewsets.ModelViewSet):
    """商品管理

    """
    queryset = Goods.objects.filter(is_deleted=False, status=0)
    serializer_class = GoodsSerializer

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
