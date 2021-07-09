# coding: utf-8

"""用户"""

import datetime
from django.db import models
from django_jsonfield_backport.models import JSONField
from libs.django.db.models import FixedCharField, BinaryCharFiled, TinyIntField, TextField, LongTextField
from libs.django.db.enum import TypeFieldEnum, first_value_unique
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
    password = models.CharField(verbose_name='密码', max_length=50, null=False)
    is_deleted = models.BooleanField(verbose_name='已删除', null=False, default=0)  # 0未删除 1已删除
    create_time = models.DateTimeField(verbose_name='创建时间', null=False, default=datetime.datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', null=False, default=datetime.datetime.now)


class Xxx(models.Model):

    class Meta:

        # 实际表名以 `t_` 为前缀
        db_table = 't_xxx'
        # ORM表注释
        verbose_name = 'xxx表'
        # 联合索引
        index_together = ('xxx_type', 'xxx_name')

    @first_value_unique
    class XxxTypeEnum(TypeFieldEnum):
        """ xxx类型枚举类 """

        TYPE_ONE = (1, '类型1')
        TYPE_TWO = (2, '类型2')
        TYPE_THREE = (3, '类型3')

    # 主键自增id，要求使用bigint且业务无关
    id = models.BigAutoField(primary_key=True)
    # 某某某id使用uuid，固定32位长度，唯一键
    xxx_id = FixedCharField(verbose_name='xxxid', max_length=32, null=False, default=make_uuid, unique=True)
    # 类型字段建议使用tinyint，针对choices扩展出枚举类，方便管理
    xxx_type = TinyIntField(verbose_name='xxx类型', null=False, default=XxxTypeEnum.TYPE_ONE.val,
                            choices=XxxTypeEnum.to_tuple())
    # varchar类型统一定义成 not null default ''
    xxx_name = models.CharField(verbose_name='xxx名称', max_length=50, null=False, default='')
    # varchar binary，区分大小写
    xxx_name_bin = BinaryCharFiled(verbose_name='xxx名称（区分大小写）', max_length=50, null=False, default='')
    # 每个表必加的三个字段
    # 是否已删除，使用ORM布尔类型，对应mysql的tinyint
    is_deleted = models.BooleanField(verbose_name='是否已删除', null=False, default=0)
    # 模型创建时自动更新
    create_time = models.DateTimeField(verbose_name='创建时间', null=False, auto_now_add=True)
    # 模型修改时自动更新，注意：直接update时不触发
    update_time = models.DateTimeField(verbose_name='更新时间', null=False, auto_now=True)

    """生成的表结构
    CREATE TABLE `t_xxx` (
      `id` bigint(20) NOT NULL AUTO_INCREMENT,
      `xxx_id` char(32) NOT NULL,
      `xxx_type` tinyint(4) NOT NULL,
      `xxx_name` varchar(50) NOT NULL,
      `is_deleted` tinyint(1) NOT NULL,
      `create_time` datetime(6) NOT NULL,
      `update_time` datetime(6) NOT NULL,
      PRIMARY KEY (`id`),
      UNIQUE KEY `xxx_id` (`xxx_id`),
      KEY `t_xxx_xxx_type_xxx_name_1318ffcb_idx` (`xxx_type`,`xxx_name`)
    ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4   
    """


class XxxDetail(models.Model):
    """xxx子表（详情表）

    有些情况，需要将大字段从源表中垂直拆分出来，形成一个子表，以减少查询I/O
    """

    class Meta:

        db_table = 't_xxx_detail'
        verbose_name = 'xxx详情表'

    id = models.BigAutoField(primary_key=True)
    '''一对一外键（源表唯一键）使用 `models.OneToOneField`
        外键 to='Xxx' 一律使用源表模型类的字符串形式，不允许出现 to=Xxx，避免出现定义先后顺序不同导致报错
        必须加 db_constraint=False，避免建立数据库层面的外键约束
        on_delete由于实际场景为逻辑删除，不会出现delete，不做要求
    '''
    xxx = models.OneToOneField('Xxx', to_field='xxx_id', verbose_name='xxxid', on_delete=models.CASCADE, db_constraint=False)
    '''大字段类型
        django自带的TextField为mysql的longtext，这里使用真实的TextField
        大字段类型统一设置 null=True
    '''
    content = TextField(verbose_name='内容', null=True)
    long_content = LongTextField(verbose_name='长内容', null=True)
    name_list = JSONField(verbose_name='名称列表', null=True)

    """生成的表结构
    CREATE TABLE `t_xxx_detail` (
      `id` bigint(20) NOT NULL AUTO_INCREMENT,
      `content` text,
      `long_content` longtext,
      `name_list` json DEFAULT NULL,
      `xxx_id` char(32) NOT NULL,
      PRIMARY KEY (`id`),
      UNIQUE KEY `xxx_id` (`xxx_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """


class Yyy(models.Model):

    class Meta:

        db_table = 't_yyy'
        verbose_name = 'yyy表'

    id = models.BigAutoField(primary_key=True)
    yyy_id = FixedCharField(verbose_name='yyyid', max_length=32, null=False, default=make_uuid, unique=True)
    '''多对一外键使用 `models.ForeignKey`
        外键 to='Xxx' 一律使用源表模型类的字符串形式，不允许出现 to=Xxx，避免出现定义先后顺序不同导致报错
        必须加 db_constraint=False，避免建立数据库层面的外键约束
        on_delete由于实际场景为逻辑删除，不会出现delete，不做要求
        null值的定义：
            True:  关联查询默认使用 INNER JOIN
            False: 关联查询默认使用 LEFT JOIN
    '''
    xxx = models.ForeignKey('Xxx', to_field='xxx_id', verbose_name='xxxid', null=True, on_delete=models.CASCADE, db_constraint=False)
    is_deleted = models.BooleanField(verbose_name='是否已删除', null=False, default=0)
    create_time = models.DateTimeField(verbose_name='创建时间', null=False, auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', null=False, auto_now=True)

    """生成的表结构
    CREATE TABLE `t_yyy` (
      `id` bigint(20) NOT NULL AUTO_INCREMENT,
      `yyy_id` char(32) NOT NULL,
      `is_deleted` tinyint(1) NOT NULL,
      `create_time` datetime(6) NOT NULL,
      `update_time` datetime(6) NOT NULL,
      `xxx_id` char(32) NOT NULL,
      PRIMARY KEY (`id`),
      UNIQUE KEY `yyy_id` (`yyy_id`),
      KEY `t_yyy_xxx_id_ef705c68` (`xxx_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """
