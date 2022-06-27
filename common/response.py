"""
response.py
"""


def make_response(data=None, errcode=0, errmsg='success', **kwargs):
    """返回"""
    res = {
        'errcode': errcode,
        'errmsg': errmsg
    }
    if data is not None:
        res['data'] = data
    return {**res, **kwargs}


if __name__ == '__main__':
    pass
