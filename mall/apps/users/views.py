from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import User


class UserAPIView(APIView):
    def get(self, request, username):
        user = User.objects.filter(user=username)
        user_dict = user.get_serializer(user)
        user_dict["username"] = username
        return Response(user_dict)
