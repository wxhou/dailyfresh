from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from common.models import BaseModel
from common.choices import SEX, MESSAGE_CHOICES


# Create your models here.

class User(AbstractUser):
    name = models.CharField(_('username'), max_length=30, null=True, blank=True, help_text="姓名")
    birthday = models.DateField(_('birthday'), null=True, blank=True, help_text="出生年月")
    gender = models.CharField(_('gender'), max_length=6, choices=SEX, default="female", help_text="性别")
    mobile = models.CharField(_('phone'), null=True, blank=True, max_length=11, help_text="电话")
    email = models.EmailField(_('email'), unique=True, max_length=128, null=True, blank=True, help_text="邮箱")
    avatar = models.ImageField(_('avatar'), upload_to="avatar/", help_text="用户头像")

    class Meta:
        db_table = 'user'
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCode(BaseModel):
    """
    短信验证码
    """
    code = models.CharField(_('code'), max_length=10, help_text="验证码")
    mobile = models.CharField(_('mobile'), max_length=11, help_text="手机号码")

    class Meta:
        db_table = 'user_verify_code'
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code


class UserFav(BaseModel):
    """
    用户收藏
    """
    user = models.ForeignKey(User, help_text='用户ID', on_delete=models.CASCADE)
    goods = models.ForeignKey('goods.Goods', help_text="商品ID", on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_fav'
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name
        unique_together = ("user", "goods")

    def __str__(self):
        return self.user.username


class UserLeavingMessage(BaseModel):
    """
    用户留言
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_type = models.PositiveSmallIntegerField(_('message type'), default=1, choices=MESSAGE_CHOICES,
                                                    help_text=u"留言类型: 1(留言),2(投诉),3(询问),4(售后),5(求购)")
    subject = models.CharField(_('subject'), max_length=100, default="", help_text="主题")
    content = models.TextField(_('message content'), default="", help_text="留言内容")
    file = models.ImageField(_('upload message image'), upload_to="message/", help_text="上传的图片")

    class Meta:
        db_table = 'user_message'
        verbose_name = "用户留言"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject


class UserAddress(BaseModel):
    """
    用户收货地址
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    province = models.CharField(_('province'), max_length=100, default="", help_text="省份")
    city = models.CharField(_('city'), max_length=100, default="", help_text="城市")
    district = models.CharField(_('district'), max_length=100, default="", help_text="区域")
    address = models.CharField(_('address'), max_length=100, default="", help_text="详细地址")
    signer_name = models.CharField(_('signer_name'), max_length=100, default="", help_text="签收人")
    signer_mobile = models.CharField(_('signer_mobile'), max_length=11, default="", help_text="电话")

    class Meta:
        db_table = 'user address'
        verbose_name = "收货地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address
