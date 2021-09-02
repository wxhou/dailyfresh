from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
from common.models import BaseModel
from common.choices import CATEGORY_TYPE


# Create your models here.


class GoodsCategory(BaseModel):
    """
    商品类别
    """
    name = models.CharField(_('category name'), default="", max_length=30, help_text="类别名")
    code = models.CharField(_('category code'), default="", max_length=30, help_text="类别code")
    desc = models.TextField(_('category desc'), default="", help_text="类别描述")
    category_type = models.IntegerField(_('category level'), choices=CATEGORY_TYPE, help_text="类目级别")
    parent_category = models.ForeignKey("self", null=True, blank=True, help_text="父类目级别",
                                        related_name="sub_cat", on_delete=models.CASCADE)
    navigation = models.BooleanField(_("navigation"), default=False, help_text="是否导航")

    class Meta:
        db_table = "goods_category"
        verbose_name = "商品类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(BaseModel):
    """
    品牌名
    """
    category = models.ForeignKey(GoodsCategory, null=True, blank=True,
                                 on_delete=models.CASCADE, help_text="商品类目")
    name = models.CharField(_("brand name"), default="", max_length=30, help_text="品牌名")
    desc = models.TextField(_('brand desc'), default="", max_length=200, help_text="品牌描述")
    image = models.ImageField(upload_to="brands/", max_length=200, help_text='品牌图片')

    class Meta:
        db_table = "goods_brand"
        verbose_name = "品牌"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(BaseModel):
    """
    商品
    """
    category = models.ForeignKey(GoodsCategory, related_name='category', on_delete=models.CASCADE, help_text="商品类目")
    goods_sn = models.CharField(_('goods sn'), max_length=50, default="", help_text="商品唯一货号")
    name = models.CharField(_('goods name'), max_length=100, help_text="商品名")
    click_num = models.IntegerField(_('goods click number'), default=0, help_text="点击数")
    sold_num = models.IntegerField(_('goods sold number'), default=0, help_text="商品销售量")
    fav_num = models.IntegerField(_('fav number'), default=0, help_text="收藏数")
    goods_num = models.IntegerField(_('goods num'), default=0, help_text="库存数")
    market_price = models.FloatField(_('market price'), default=0, help_text="市场价格")
    shop_price = models.FloatField(_('goods shop price'), default=0, help_text="本店价格")
    goods_brief = models.TextField(_('goods brief'), max_length=500, help_text="商品简短描述")
    goods_desc = RichTextUploadingField()
    ship_free = models.BooleanField(_('ship free'), default=True, help_text="是否承担运费")
    goods_front_image = models.ImageField(_('goods front image'), upload_to="goods/cover/", null=True, blank=True,
                                          help_text="封面图")
    is_new = models.BooleanField(_('is new'), default=False, help_text="是否新品")
    is_hot = models.BooleanField(_('is hot'), default=False, help_text="是否热销")

    class Meta:
        db_table = 'goods'
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class IndexAd(BaseModel):
    category = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)

    class Meta:
        db_table = "index_ad"
        verbose_name = '首页商品类别广告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class GoodsImage(BaseModel):
    """
    商品轮播图
    """
    goods = models.ForeignKey(Goods, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(_('goods image'), upload_to="goods/image/", help_text="图片", null=True, blank=True)

    class Meta:
        db_table = 'goods_image'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(BaseModel):
    """
    轮播的商品
    """
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, help_text="商品")
    image = models.ImageField(upload_to='goods/banner/', verbose_name="轮播图片")
    index = models.IntegerField(default=0, verbose_name="轮播顺序")

    class Meta:
        db_table = 'goods_banner'
        verbose_name = '轮播商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class HotSearchWords(BaseModel):
    """
    热搜词
    """
    keywords = models.CharField(_('keyword'), default="", max_length=20, help_text="热搜词")
    index = models.IntegerField(_('order'), default=0, help_text="排序")

    class Meta:
        db_table = 'goods_hot_word'
        verbose_name = '热搜词'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords
