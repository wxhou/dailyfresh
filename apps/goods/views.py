from rest_framework import mixins
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from apps.goods.models import Goods, GoodsCategory, Banner, HotSearchWords
from .serializers import (CategoryDetailSerializer, GoodsDetailSerializer,
                          HotWordSerializer, BannerSerializer)


# Create your views here.

class GoodsCategoryViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    """商品分类管理
    list:
        获取商品分类列表

        ---

    retrieve:
        获取商品分类详情

        ---

    """
    queryset = GoodsCategory.objects.filter(category_type=1, is_deleted=False, status=0)
    serializer_class = CategoryDetailSerializer


class GoodsPagination(PageNumberPagination):
    """商品分页器"""
    page_size = 12
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100


class GoodsViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """商品管理
    list:
        商品列表

        ---

    retrieve:
        商品详情

        ---
    """
    queryset = Goods.objects.filter(is_deleted=False, status=0).order_by('id')
    serializer_class = GoodsDetailSerializer
    pagination_class = GoodsPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name", "goods_brief", "goods_desc")  # 搜索
    ordering_fields = ("sold_num", 'shop_price')  # 排序

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class HotWordViewSet(mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """热搜词列表
    list:
        热搜词列表

        ---
    """
    queryset = HotSearchWords.objects.filter(is_deleted=False, status=0)
    serializer_class = HotWordSerializer


class BannerViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """轮播图列表
    list:
        轮播图列表

        ---
    """
    queryset = Banner.objects.filter(is_deleted=False, status=0).order_by('index')
    serializer_class = BannerSerializer
