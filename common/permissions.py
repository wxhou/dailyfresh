#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging
from rest_framework import permissions

logger = logging.getLogger('debug')


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        logger.debug("{} == {}".format(obj.user, request.user))
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
