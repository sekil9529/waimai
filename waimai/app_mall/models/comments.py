# coding: utf-8

"""评论"""

import datetime
from django.db import models
from jsonfield import JSONField
from collections import defaultdict

from .items import Item
from libs.django.db.models import FixedCharField, TinyIntField
from libs.uuid import make_uuid
from libs.dict import ExtDict

__all__ = (
    'ShopComment',
    'ShopCommentDetails',
    'ShopCommentLike',
)


class ShopComment(models.Model):

    class Meta:
        db_table = 't_shop_comment'
        verbose_name = '店铺评论表'

    id = models.BigAutoField(primary_key=True)
    shop_comment_id = FixedCharField('店铺评论id', max_length=32, null=False, default=make_uuid, unique=True)
    user = models.ForeignKey('app_user.User', to_field='user_id', verbose_name='用户id', null=False,
                             on_delete=models.CASCADE, db_constraint=False)
    shop = models.ForeignKey('Shop', to_field='shop_id', verbose_name='店铺id', null=False,
                             on_delete=models.CASCADE, db_constraint=False)
    is_anonymous = models.BooleanField(verbose_name='是匿名用户', null=False, default=0)  # 1匿名 0非匿名
    score_service = TinyIntField(verbose_name='服务分值', null=False, default=0)  # 1-5
    score_taste = TinyIntField(verbose_name='口味分值', null=False, default=0)  # 1-5
    score_pack = TinyIntField(verbose_name='包装分值', null=False, default=0)  # 1-5
    score_deliver = TinyIntField(verbose_name='配送分值', null=False, default=0)  # 1-5
    is_deleted = models.BooleanField(verbose_name='已删除', null=False, default=0)  # 0未删除 1已删除
    create_time = models.DateTimeField(verbose_name='创建时间', null=False, default=datetime.datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', null=False, default=datetime.datetime.now)

    @property
    def content(self):
        """评论内容"""
        obj = ShopCommentDetails.objects.filter(shop_comment_id=self.shop_comment_id).only('content').first()
        if obj:
            return obj.content or ''
        return ''

    @property
    def reply_content(self):
        """商家回复内容"""
        obj = ShopCommentDetails.objects.filter(shop_comment_id=self.shop_comment_id).only('reply_content').first()
        if obj:
            return obj.reply_content or ''
        return ''

    @property
    def image_list(self):
        """图片列表"""
        obj = ShopCommentDetails.objects.filter(shop_comment_id=self.shop_comment_id).only('image_list').first()
        if obj:
            return obj.image_list or []
        return []

    def at_item_info_list(self):
        """at商品信息列表"""
        obj = ShopCommentDetails.objects.filter(shop_comment_id=self.shop_comment_id).only('at_item_id_list').first()
        if not obj:
            return []
        # 商品信息
        info = defaultdict(ExtDict)
        queryset = Item.objects.filter(is_deleted=0, item_id__in=obj.at_item_id_list).all()
        for obj in queryset:
            elem = info[obj.item_id]
            elem.itemId = str(obj.item_id)
            elem.name = obj.name
        dto_list = [info[item_id] for item_id in obj.at_item_id_list if item_id in info]
        return dto_list


class ShopCommentDetails(models.Model):

    class Meta:
        db_table = 't_shop_comment_details'
        verbose_name = '店铺评论详情表'

    id = models.BigAutoField(primary_key=True)
    shop_comment = models.ForeignKey('ShopComment', to_field='shop_comment_id', verbose_name='店铺评论id', null=False,
                                     on_delete=models.CASCADE, db_constraint=False, unique=True)
    image_list = JSONField(verbose_name='评论图片列表', null=True)
    at_item_id_list = JSONField(verbose_name='at商品id列表', null=True)
    content = models.CharField(verbose_name='评论内容', max_length=2000, null=True)
    reply_content = models.CharField(verbose_name='商家回复', max_length=2000, null=True)
    is_deleted = models.BooleanField(verbose_name='已删除', null=False, default=0)  # 0未删除 1已删除
    create_time = models.DateTimeField(verbose_name='创建时间', null=False, default=datetime.datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', null=False, default=datetime.datetime.now)


class ShopCommentLike(models.Model):

    class Meta:
        db_table = 't_shop_comment_like'
        verbose_name = '店铺评论点赞表'

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('app_user.User', to_field='user_id', verbose_name='用户id', null=False,
                             on_delete=models.CASCADE, db_constraint=False)
    shop_comment = models.ForeignKey('ShopComment', to_field='shop_comment_id', verbose_name='店铺评论id', null=False,
                                     on_delete=models.CASCADE, db_constraint=False)
    is_deleted = models.BooleanField(verbose_name='已删除', null=False, default=0)  # 0未删除 1已删除
    create_time = models.DateTimeField(verbose_name='创建时间', null=False, default=datetime.datetime.now)
    update_time = models.DateTimeField(verbose_name='更新时间', null=False, default=datetime.datetime.now)
