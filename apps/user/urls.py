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
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from apps.user import views

app_name = 'user'

router = DefaultRouter()
router.register(r'user', views.UserAPIViewSet, basename='user')
router.register(r'login', views.LoginViewSet, basename='login')
router.register(r'collect', views.UserCollectViewSet, basename='collect')
router.register(r'message', views.UserMessageViewSet, basename='message')
router.register(r'address', views.UserAddressViewSet, basename='address')

urlpatterns = [
  path('active/<str:token>', views.active_user, name='active'),
  path('logout/', views.LogoutAPIView.as_view(), name='logout'),
  path('user/avatar/', views.UserAvatarView.as_view(), name='avatar')
] + router.urls
