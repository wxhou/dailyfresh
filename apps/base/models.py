from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


# Create your models here.
class FileModel(models.Model):
    uid = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, help_text='用户')
    fileName = models.CharField(_('fileName'), max_length=128, help_text='文件名')
    file = models.FileField(_('fileUrl'), upload_to='%Y%m%d/', help_text='文件路径')
    uniqueId = models.CharField(_('uniqueId'), max_length=128, help_text='唯一ID')
    created_time = models.DateTimeField(_('create time'), auto_now_add=True, help_text='创建时间')
    is_deleted = models.BooleanField(_('is deleted'), default=False, help_text='是否删除')

    class Meta:
        db_table = 'db_fileInfo'
        verbose_name = '文件信息'
        verbose_name_plural = verbose_name
