# -*-coding:utf-8-*-

import datetime
from typing import Optional, Any
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import QuerySet
from collections.abc import ValuesView, KeysView


class JsonEncoder(DjangoJSONEncoder):
    """json编码器"""
    def default(self, o: Any) -> Any:
        if isinstance(o, datetime.datetime):  # datetime类型
            return o.isoformat(sep=' ')
            # return to_unix_timestamp(o)  # 时间戳
        elif isinstance(o, datetime.date):  # date类型
            return o.isoformat()
        elif isinstance(o, QuerySet):  # Django QS
            return list(o)
        elif isinstance(o, set):  # 集合
            return list(o)
        elif isinstance(o, (KeysView, ValuesView)):  # dict_keys, dict_values
            return list(o)
        else:
            return super(JsonEncoder, self).default(o)


def response_ok(data: Optional[dict] = None) -> JsonResponse:
    """成功返回"""
    info = {
        'code': '0',  # 错误码
        'response': 'ok',  # 信息
        'data': data or {},  # 数据
        'desc': '成功'  # 描述
    }
    return JsonResponse(data=info, encoder=JsonEncoder)


def response_fail(code: str = '500', error: str = 'ServerError', desc: str = '服务器异常',
                  message: str = '服务异常，请稍后重试') -> JsonResponse:
    """失败返回

    :param code: 错误码
    :param error: 错误信息（英文，开发人员展示）
    :param desc: 错误描述（中文，开发人员展示）
    :param message: 错误信息（用户展示）
    :return:
    """
    info = {
        'code': str(code),
        'response': 'fail',
        'error': error,  # 错误
        'desc': desc,
        'message': message
    }
    return JsonResponse(data=info, encoder=JsonEncoder)
