import os
import sys

from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User

class UserAPIView(APIView):
    def get(self, request, username):
        user = User.objects.filter(username=username).count()
        user_dict = {}
        user_dict["count"] = user
        user_dict["username"] = username
        return Response(user_dict)

class xxx():
    pass
# 1 前端需要提供： 用户名, 两次密码, 手机号,  短信验证码, 是否同意用户协议
# 2 继承createAIPView
