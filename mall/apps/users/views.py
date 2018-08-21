import os
import sys

from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializer import UserSerializer
from .models import User

class UserAPIView(APIView):
    def get(self, request, username):
        user = User.objects.filter(username=username).count()
        user_dict = {}
        user_dict["count"] = user
        user_dict["username"] = username
        return Response(user_dict)


class MobileAPIView(APIView):
    def get(self, request, mobile):
        mobile = User.objects.filter(mobile=mobile).count()
        data = {
            "count":mobile,
            "mobile": mobile
        }
        return Response(data=data)

class CreateUserAPIView(CreateAPIView):
    """验证并创建User用户信息"""
    serializer_class = UserSerializer
# 1 前端需要提供： 用户名, 两次密码, 手机号,  短信验证码, 是否同意用户协议
# 2 继承CreateAIPView
# 3 调用验证
