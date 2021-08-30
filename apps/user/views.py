from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from .models import User, VerifyCode
from .serializers import SmsSerializer, UserRegisterSerializer


# Create your views here.


class CustomBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None


class UserRegisterViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """用户注册"""
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(is_active=True)


class UserViewSet():
    pass