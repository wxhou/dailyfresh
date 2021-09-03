import logging
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from common.errors import System, Account
from common.permissions import IsOwnerOrReadOnly
from common.response import response_ok, response_err
from utils.timekit import timedelta_from_now
from apps.user.models import User, VerifyCode, UserFav, UserLeavingMessage, UserAddress
from .serializers import (LoginSerializer, UserRegisterSerializer, UserDetailSerializer,
                          UserFavSerializer, UserFavDetailSerializer,
                          UserMessageSerializer, UserAddressSerializer)
from .tasks import send_register_email

# Create your views here.
logger = logging.getLogger('debug')


class LoginViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = LoginSerializer


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    retrieve:
        获取用户详情

        ---
    create:
        添加留言

        ---
    destroy:
    """
    queryset = User.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegisterSerializer
        return UserDetailSerializer

    def get_permissions(self):
        if self.action == 'create':
            return []
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """
        注册用户

        ---
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        token = Token.objects.get(user=user)
        # cache.set("register_token_%s" % token.key, user.pk, 30 * 60)  # 30分钟
        register_url = self.request.build_absolute_uri(reverse('user:active', args=(token.key,)))
        logger.info("register_url is : {}".format(register_url))
        send_register_email.delay(register_url, user.email)


@api_view()
@authentication_classes([])
@permission_classes([])
def active_user(request, token):
    """
    激活用户

    ---
    """
    authtoken = Token.objects.get(key=token)
    user = authtoken.user
    if user.is_active:
        return Response(response_ok(data="请勿重复注册"), status=status.HTTP_200_OK)
    if user is None:
        return Response(response_err(errcode=Account.TOKEN, errmsg=_("register code is None")))
    if timedelta_from_now(settings.REGISTER_CONFIRM_TIMEDELTA) > authtoken.created:
        return Response(response_err(Account.REGISTER_ERROR, errmsg=_('The registration message has expired')))
    user.is_active = True
    user.save()
    return Response(response_ok(data=_("active user {} success".format(user.username))))


class UserCollectViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    """
    list:
        获取用户收藏列表

        ---
    retrieve:
        收藏详情

        ---
    create:
        用户新增收藏商品

        ---
    destroy:
        删除收藏商品

        ---
    """
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    lookup_field = 'goods_id'

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return UserFav.objects.none()
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        return UserFavSerializer


class UserMessageViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    """用户留言
    create:
        添加新的留言

        ---
    list:
        留言列表

        ---
    retrieve:
        留言详情

        ---
    """
    serializer_class = UserMessageSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return UserLeavingMessage.objects.none()
        return UserLeavingMessage.objects.filter(is_deleted=False, status=0, user=self.request.user)


class UserAddressViewSet(viewsets.ModelViewSet):
    """用户收货地址管理
    create:
        添加新的收货地址

        ---
    list:
        收货地址列表

        ---
    retrieve:
        收货地址详情

        ---
    destroy:
        删除收货地址

        ---
    """
    serializer_class = UserAddressSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # queryset just for schema generation metadata
            return UserAddress.objects.none()
        return UserAddress.objects.filter(user=self.request.user, is_deleted=False, status=0)
