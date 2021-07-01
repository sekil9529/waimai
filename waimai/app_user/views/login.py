# coding: utf-8

from rest_framework.views import APIView

from app_user.models.users import User
from libs.django.response import response_ok


class PasswordLoginView(APIView):
    """密码登录"""

    authentication_classes = []

    def post(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')
        obj = User.objects.filter(is_deleted=0, phone=phone).only('password').first()
        if not obj:
            pass  # 注册
        elif obj.password != password:
            pass  # 密码错误
        pass  # 登录
        return response_ok()


class CaptchaLoginView(APIView):
    """验证码登录"""

    authentication_classes = []

    def post(self, request):
        phone = request.data.get('phone')
        captcha = request.data.get('captcha')
        if False:
            pass  # 无效验证码
        is_exists_user = User.objects.filter(is_deleted=0, phone=phone).exists()
        if not is_exists_user:
            pass  # 注册
        pass  # 登录
        return response_ok()
