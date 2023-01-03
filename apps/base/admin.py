from django.contrib import admin
from .models import FileModel

# Register your models here.
admin.site.register(FileModel)
admin.site.site_header = '每日新鲜'
admin.site.site_title = '每日新鲜'
