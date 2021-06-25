# coding: utf-8

"""店铺"""

import datetime
from django.db import models
# from django.contrib.gis.db import models
# exception：django.core.exceptions.ImproperlyConfigured: Could not find the GDAL library

from libs.django.db.models import FixedCharField
from libs.datetime import get_date_1th_of_current_month
from libs.uuid import make_uuid


class ConfigShopCategory(models.Model):

    class Meta:
        db_table = 't_config_shop_category'
        verbose_name = '店铺分类配置表'

    id = models.BigAutoField(primary_key=True)
    category_id = FixedCharField(verbose_name='分类id', max_length=32, null=False, default=make_uuid, unique=True)
    name = models.CharField(verbose_name='类型名称', max_length=255, null=False, default='')
    is_deleted = models.BooleanField(verbose_name='已删除', null=False, default=0)  # 0未删除 1已删除
    create_time = models.DateTimeField(verbose_name='创建时间', null=False, default=datetime.datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', null=False, default=datetime.datetime.now)


class Shop(models.Model):

    class Meta:
        db_table = 't_shop'
        verbose_name = '店铺表'

    id = models.BigAutoField(primary_key=True)
    shop_id = FixedCharField(verbose_name='店铺id', max_length=32, null=False, default=make_uuid, unique=True)
    name = models.CharField(verbose_name='店铺名称', max_length=255, null=False, default='')
    logo = models.CharField(verbose_name='logo', max_length=255, null=False, default='')
    branch_name = models.CharField(verbose_name='分店名称', max_length=255, null=False, default='')
    score = models.IntegerField(verbose_name='评分', null=False, default=0)
    category = models.ForeignKey('ConfigShopCategory', to_field='category_id', verbose_name='店铺分类id', null=False,
                                 on_delete=models.CASCADE, db_constraint=False)
    # location = models.PointField(verbose_name='位置', null=True)
    address = models.CharField(verbose_name='店铺地址', max_length=255, null=False)
    latitude = models.DecimalField(verbose_name='纬度', max_digits=9, decimal_places=6, default=0, null=False)
    longitude = models.DecimalField(verbose_name='经度', max_digits=9, decimal_places=6, default=0, null=False)
    start_price = models.DecimalField(verbose_name='起送价', max_digits=7, decimal_places=2, default=0, null=False)
    deliver_price = models.DecimalField(verbose_name='配送费', max_digits=7, decimal_places=2, default=0, null=False)
    is_brand = models.BooleanField(verbose_name='是品牌', null=False, default=0)  # 0非品牌 1是品牌
    start_time = models.TimeField(verbose_name='营业起始时间', null=False)
    end_time = models.TimeField(verbose_name='营业结束时间', null=False)
    is_deleted = models.BooleanField(verbose_name='已删除', null=False, default=0)  # 0未删除 1已删除
    create_time = models.DateTimeField(verbose_name='创建时间', null=False, default=datetime.datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', null=False, default=datetime.datetime.now)

    @property
    def month_sales(self):
        """月销量"""
        date_1th = get_date_1th_of_current_month()
        obj = ShopSales.objects.filter(is_deleted=0, shop_id=self.id, date_1=date_1th).first()
        return obj.sales if obj else 0


class ShopSales(models.Model):

    class Meta:
        db_table = 't_shop_sales'
        verbose_name = '店铺销量表'
        unique_together = (
            ('shop', 'date_1')
        )

    id = models.BigAutoField(primary_key=True)
    shop = models.ForeignKey('Shop', to_field='shop_id', verbose_name='店铺id', null=False,
                             on_delete=models.CASCADE, db_constraint=False)
    # 仅存一号
    date_1 = models.DateField(verbose_name='日期', null=False, default=get_date_1th_of_current_month)
    sales = models.IntegerField(verbose_name='销量', null=False, default=1)
    is_deleted = models.BooleanField(verbose_name='已删除', null=False, default=0)  # 0未删除 1已删除
    create_time = models.DateTimeField(verbose_name='创建时间', null=False, default=datetime.datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', null=False, default=datetime.datetime.now)

