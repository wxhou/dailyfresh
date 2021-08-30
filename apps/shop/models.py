from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import BaseModel
from common.choices import ORDER_STATUS


# Create your models here.


class ShoppingCart(BaseModel):
    """
    购物车
    """
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, help_text=u"用户")
    goods = models.ForeignKey("goods.Goods", on_delete=models.CASCADE, help_text=u"商品")
    nums = models.IntegerField(_('shop number'), default=0, help_text="购买数量")

    class Meta:
        db_table = 'shop_car'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=('user', 'goods'), name='unique goods user')
        ]

    def __str__(self):
        return "%s(%d)".format(self.goods.name, self.nums)


class OrderInfo(BaseModel):
    """
    订单
    """
    user = models.ForeignKey("user.User", verbose_name="用户", on_delete=models.CASCADE)
    order_sn = models.CharField(_('order sn'), max_length=30, null=True, blank=True, unique=True, help_text="订单号")
    trade_no = models.CharField(_('trade no'), max_length=100, unique=True, null=True, blank=True, help_text="交易号")
    pay_status = models.CharField(_('pay status'), choices=ORDER_STATUS, default="paying", max_length=30,
                                  help_text="订单状态")
    post_script = models.CharField(_('post script'), max_length=200, help_text="订单留言")
    order_mount = models.FloatField(_('order mount'), default=0.0, help_text="订单金额")
    pay_time = models.DateTimeField(_('pay time'), null=True, blank=True, help_text="支付时间")

    # 用户信息
    address = models.CharField(_('address'), max_length=100, default="", help_text="收货地址")
    signer_name = models.CharField(_('signer name'), max_length=20, default="", help_text="签收人")
    singer_mobile = models.CharField(_('singer mobile'), max_length=11, help_text="联系电话")

    class Meta:
        db_table = 'shop_order'
        verbose_name = u"订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderGoods(BaseModel):
    """
    订单的商品详情
    """
    order = models.ForeignKey(OrderInfo, help_text="订单信息", on_delete=models.CASCADE)
    goods = models.ForeignKey("goods.Goods", help_text="商品", on_delete=models.CASCADE)
    goods_num = models.IntegerField(_('goods number'), default=0, help_text="商品数量")

    class Meta:
        db_table = 'shop_goods'
        verbose_name = "订单商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)
