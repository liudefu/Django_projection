# coding=utf-8
from django.conf.urls import url

from users.views import *

urlpatterns = [
    url(r"^usernames/(?P<username>\w{5,20})/count/$", UserAPIView.as_view(), name="username"),
    url(r'^phones/(?P<mobile>1[345789]\d{9})/count/$', MobileAPIView.as_view(),name='phonecount'),
    url(r"^$", CreateUserAPIView.as_view(), name="create_user"),
]
