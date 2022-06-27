"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('goods/', include('goods.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api-auth/', include('rest_framework.urls'))
]

if settings.DEBUG:
    # from django.conf.urls.static import static
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    schema_view = get_schema_view(
        openapi.Info(
            title='dailyfresh',
            default_version='v2',
            description="dailyfresh",
            terms_of_service="https://www.cnblog.com/wxhou",
            contact=openapi.Contact(email="1084502012@qq.com"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$',
                schema_view.without_ui(cache_timeout=0), name='schema-json'),
        re_path(r'^swagger/$', schema_view.with_ui('swagger',
                                                   cache_timeout=0), name='schema-swagger-ui'),
        re_path(r'^redoc/$', schema_view.with_ui('redoc',
                                                 cache_timeout=0), name='schema-redoc'),
    ]
