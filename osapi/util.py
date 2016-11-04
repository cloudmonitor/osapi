# _*_ coding:utf-8 _*_

import datetime, time
import functools

from flask import request

from settings import *
from ceilometer import get_localtime,localtime_to_utc


THREE_HOUR = 28740


def auth_is_available_bak(token):
    """认证token是否有效"""
    date_time = time.strptime(str(datetime.datetime.now())[:16], "%Y-%m-%d %H:%M")
    issued_time = time.strptime(str(token['issued_at']).replace('T', ' ')[:16], "%Y-%m-%d %H:%M")
    expires_time = time.strptime(str(token['expires']).replace('T', ' ')[:16], "%Y-%m-%d %H:%M")
    date_time_seconds = time.mktime(date_time) - THREE_HOUR
    issued_time_seconds = time.mktime(issued_time)
    expires_time_seconds = time.mktime(expires_time)
    if date_time_seconds >= issued_time_seconds and  date_time_seconds <= expires_time_seconds:
        return True
    else:
        return False


def auth_is_available(func):
    """认证admin_token是否有效的装饰器"""
    @functools.wraps(func)
    def authority(*args, **kwargs):
        error_info = {}
        token = json.loads(request.args.get('token'))
        date_time = time.strptime(str(datetime.datetime.now())[:16], "%Y-%m-%d %H:%M")
        issued_time = time.strptime(str(token['issued_at']).replace('T', ' ')[:16], "%Y-%m-%d %H:%M")
        expires_time = time.strptime(str(token['expires']).replace('T', ' ')[:16], "%Y-%m-%d %H:%M")
        date_time_seconds = time.mktime(date_time) - THREE_HOUR
        issued_time_seconds = time.mktime(issued_time)
        expires_time_seconds = time.mktime(expires_time)
        if date_time_seconds >= issued_time_seconds and  date_time_seconds <= expires_time_seconds:
            return_info = func(*args, **kwargs)
            return return_info
        else:
            error_info['error'] = 'not available'
            return error_info
    return authority

