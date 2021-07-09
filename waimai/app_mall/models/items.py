# coding: utf-8

"""商品"""

import datetime
from django.db import models
from django_jsonfield_backport.models import JSONField
from collections import defaultdict

from libs.django.db.models import FixedCharField
from libs.uuid import make_uuid
from libs.dict import ExtDict

__all__ = (
    'ItemMaterial',
    'Item',
)


class ItemMaterial(models.Model):

    class Meta:
        db_table = 't_item_material'
        verbose_name = '商品原料表'

    id = models.BigAutoField(primary_key=True)
    material_id = FixedCharField(verbose_name='原料id', max_length=32, null=False, default=make_uuid, unique=True)
    name = models.CharField(verbose_name='原料名称', max_length=50, null=False)
    is_deleted = models.BooleanField(verbose_name='已删除', null=False, default=0)  # 0未删除 1已删除
    create_time = models.DateTimeField(verbose_name='创建时间', null=False, default=datetime.datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', null=False, default=datetime.datetime.now)


class Item(models.Model):

    class Meta:
        db_table = 't_item'
        verbose_name = '商品表'

    id = models.BigAutoField(primary_key=True)
    item_id = FixedCharField(verbose_name='商品id', max_length=32, null=False, default=make_uuid, unique=True)
    shop = models.ForeignKey('Shop', verbose_name='店铺id', null=False, on_delete=models.CASCADE, db_constraint=False)
    logo = models.CharField(verbose_name='商品logo', max_length=255, null=False, default='')
    name = models.CharField(verbose_name='商品名称', max_length=255, null=False, default='')
    desc = models.CharField(verbose_name='商品简介', max_length=50, null=False, default='')
    origin_price = models.DecimalField(verbose_name='原价', max_digits=7, decimal_places=2, null=True)
    current_price = models.DecimalField(verbose_name='现价', max_digits=7, decimal_places=2, null=False, default=0)
    packing_price = models.DecimalField(verbose_name='打包费', max_digits=7, decimal_places=2, null=False, default=0)
    material_id_list = JSONField(verbose_name='原料id列表', null=True)
    is_deleted = models.BooleanField(verbose_name='已删除', null=False, default=0)  # 0未删除 1已删除
    create_time = models.DateTimeField(verbose_name='创建时间', null=False, default=datetime.datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', null=False, default=datetime.datetime.now)

    @property
    def material_dto_list(self):
        """原料信息列表"""
        if not self.material_id_list:
            return []
        info = defaultdict(ExtDict)
        queryset = ItemMaterial.objects.filter(is_deleted=0, material_id__in=self.material_id_list).all()
        for obj in queryset:
            elem = info[obj.material_id]
            elem.materialId = str(obj.material_id)
            elem.name = obj.name
        dto_list = [info[material_id] for material_id in self.material_id_list if material_id in info]
        return dto_list

    @property
    def material_name_list(self):
        """原料名称列表"""
        dto_list = self.material_dto_list
        return [item.name for item in dto_list]
