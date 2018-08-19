# coding=utf-8
from django.conf.urls import url

from apps.users.views import UserAPIView

urlpatterns = [
    url(r"user/(?P<username>\w{5,20})/count/", UserAPIView.as_view(), name="username")
]
