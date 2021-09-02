from django.contrib import admin
from apps.goods.models import Goods, GoodsImage, GoodsCategory, GoodsCategoryBrand, IndexAd, Banner, HotSearchWords

# Register your models here.
admin.site.register(Goods)
admin.site.register(GoodsImage)
admin.site.register(GoodsCategory)
admin.site.register(GoodsCategoryBrand)
admin.site.register(IndexAd)
admin.site.register(Banner)
admin.site.register(HotSearchWords)
