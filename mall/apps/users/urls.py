# coding=utf-8
from django.conf.urls import url

from users.views import *

urlpatterns = [
    url(r"usernames/(?P<username>\w{5,20})/count/", UserAPIView.as_view(), name="username"),
    url(r"^$", CreateUserAPIView.as_view(), name="create_user"),
]
