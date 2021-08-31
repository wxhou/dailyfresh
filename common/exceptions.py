#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging
import traceback
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from common.errors import System
from common.response import response_err

logger = logging.getLogger('debug')


class MyAPIException(APIException):
    status_code = status.HTTP_200_OK
    default_detail = _('A server error occurred.')
    default_code = 'error'
    err_code = status.HTTP_200_OK

    def __init__(self, detail=None, err_code=None):
        if err_code:
            self.err_code = err_code
        logger.debug('serializer err:{}'.format(detail))
        super(MyAPIException, self).__init__(
            detail=detail, code=self.status_code)


def my_exception_handler(exc, context):
    """处理视图异常
    try:
        正常的逻辑
    except:
        主要用来处理该处请求
    :param exc: 异常实例
    :param context:
    :return:
    """
    response = exception_handler(exc, context)
    if response is None:
        # 服务器内部错误
        logger.critical(traceback.format_exc())
        return Response(response_err(errcode=System.ERROR, errmsg=format(exc)),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # 保存错误码
    if hasattr(exc, 'err_code'):
        response.data['errcode'] = exc.err_code
        response.status_code = status.HTTP_200_OK
    detail = response.data.pop('detail', None)
    if detail is not None:
        response.data['errmsg'] = detail
    return response
