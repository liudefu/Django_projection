import os
import sys

from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
sys.path.append(os.getcwd()+"/apps")
from users.models import User


class UserAPIView(APIView):
    def get(self, request, username):
        user = User.objects.filter(username=username).count()
        user_dict = {}
        user_dict["count"] = user
        user_dict["username"] = username
        return Response(user_dict)
