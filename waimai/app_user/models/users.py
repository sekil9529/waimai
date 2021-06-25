# coding: utf-8

"""用户"""

import datetime
from django.db import models

from libs.django.db.models import FixedCharField
from libs.uuid import make_uuid

__all__ = (
    'User',
)


class User(models.Model):

    class Meta:
        db_table = 't_user'
        verbose_name = '用户表'

    id = models.BigAutoField(primary_key=True)
    user_id = FixedCharField(verbose_name='用户id', max_length=32, null=False, default=make_uuid, unique=True)
    name = models.CharField(verbose_name='用户名称', max_length=50, null=False)
    phone = models.CharField(verbose_name='手机号', max_length=50, null=False)
    is_deleted = models.BooleanField(verbose_name='已删除', null=False, default=0)  # 0未删除 1已删除
    create_time = models.DateTimeField(verbose_name='创建时间', null=False, default=datetime.datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', null=False, default=datetime.datetime.now)

