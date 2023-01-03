#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging
from rest_framework.permissions import BasePermission
from rest_framework.permissions import AllowAny, IsAuthenticated

logger = logging.getLogger('debug')


class IsStaffUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsSelfOrIsSuperUser(BasePermission):
    """
    自定义权限只允许User对象的所有者和超级用户进行编辑。
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        # isAdmin
        if request.user and request.user.is_superuser:
            return True
        if not hasattr(obj, 'user'):
            return False
        return getattr(obj, 'user') == request.user


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    1.staff
    2.is_super
    """

    def has_permission(self, request, view):
        if not request.user:
            return False
        if request.user.is_superuser:
            return True
        if request.user.is_staff:
            return True
        return False
