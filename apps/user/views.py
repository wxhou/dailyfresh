import logging
from django.conf import settings
from django.urls import reverse
from django.contrib import auth
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from rest_framework import status, parsers, views, viewsets, mixins
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema

from common.errors import Errcode
from common.response import make_response
from common.permissions import AllowAny, IsAuthenticated, IsSelfOrIsSuperUser, IsStaffUser
from utils.timekit import timedelta_from_now
from apps.user.models import User, UserFav, UserLeavingMessage, UserAddress
from apps.user.serializers import (LoginSerializer, UserAvatarSerializer,
                                   UserRegisterSerializer, UserDetailSerializer,
                                   UserFavSerializer, UserFavDetailSerializer,
                                   UserMessageSerializer, UserAddressSerializer)
from apps.user.tasks import send_register_email

# Create your views here.
logger = logging.getLogger('debug')


class LoginViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        """
        登录

        ---
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        if user is None:
            return Response(
                make_response(errcode=Errcode.USER_NOT_FOUND, errmsg=_('user not exist or username/password is error')),
                status=status.HTTP_403_FORBIDDEN)
        headers = self.get_success_headers(serializer.data)
        auth.login(self.request, user)
        refresh = RefreshToken.for_user(user)
        result = {
            "data": serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return Response(make_response(**result), status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        data = serializer.validated_data
        user = auth.authenticate(self.request, username=data['email'], password=data['password'])
        return user


class LogoutAPIView(views.APIView):
    """退出登录"""

    permission_classes = (IsAuthenticated,)

    def logout(self):
        auth.logout(self.request)
        return Response(make_response(), status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        """
        退出登录

        ---
        """
        return self.logout()

    def post(self, request, *args, **kwargs):
        """
        退出登录

        ---
        """
        return self.logout()


class UserAPIViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """
    retrieve:

        获取用户详情

        ---
    create:

        注册用户

        ---
    update:
        更新用户信息

        ---
    destroy:
    """
    # 可以通过上面的备注给swagger中添加文档
    queryset = User.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return UserRegisterSerializer
        return UserDetailSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(make_response(data=serializer.data), status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={200: UserDetailSerializer})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(make_response(errcode=status.HTTP_400_BAD_REQUEST, errmsg=serializer.errors),
                            status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(make_response(data=serializer.data), status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        token = Token.objects.get(user=user)
        cache.set("register_token_%s" % token.key, user.pk, 30 * 60)  # 30分钟
        register_url = self.request.build_absolute_uri(reverse('user:active', args=(token.key,)))
        logger.info("register_url is : {}".format(register_url))
        send_register_email.delay(register_url, user.email)


class UserAvatarView(views.APIView):
    parser_classes = (parsers.FormParser, parsers.MultiPartParser)
    permission_classes = (IsSelfOrIsSuperUser,)

    @swagger_auto_schema(request_body=UserAvatarSerializer)
    def post(self, request, *args, **kwargs):
        """
        上传头像

        ---
        """
        serializer = UserAvatarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        user.avatar = serializer.validated_data['avatar']
        user.save()
        return Response(make_response(serializer.data), status=status.HTTP_200_OK)


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
    if user is None:
        return Response(make_response(errcode=Errcode.USER_NOT_FOUND, errmsg=_("register code is None")))
    if user.is_active:
        return Response(make_response(data="请勿重复注册"), status=status.HTTP_200_OK)
    if timedelta_from_now(days=settings.REGISTER_CONFIRM_TIMEDELTA) > authtoken.created:
        return Response(make_response(Errcode.REGISTER_ERROR, errmsg=_('The registration message has expired')))
    user.is_active = True
    user.save()
    return Response(make_response(data=_("active user {} success".format(user.username))))


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
    permission_classes = (IsSelfOrIsSuperUser,)
    lookup_field = 'goods_id'

    def get_queryset(self):
        # if getattr(self, 'swagger_fake_view', False):
        #     # queryset just for schema generation metadata
        #     return UserFav.objects.none()
        return UserFav.objects.filter(to_user=self.request.user.id)

    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        return UserFavSerializer


class UserMessageViewSet(viewsets.ModelViewSet):
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
    parser_classes = (parsers.FormParser, parsers.MultiPartParser)
    permission_classes = (IsSelfOrIsSuperUser,)

    def get_queryset(self):
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
    permission_classes = (IsSelfOrIsSuperUser,)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user, is_deleted=False, status=0)
