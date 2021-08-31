"""
response.py
"""


def response_ok(data=None, **kwargs):
    """正确返回"""
    resp = {"errcode": 0, "errmsg": 'success'}
    if data:
        resp['data'] = data
    return {**resp, **kwargs}


def response_err(errcode=None, errmsg=''):
    """错误返回"""
    return {"errcode": errcode, "errmsg": errmsg}
