# coding=utf-8
from django.conf.urls import url

from oauth.views import *

urlpatterns = [
    url(r"^qq/statues/$", OauthQQView.as_view(), name="qq_statues"),
    url(r"^qq/users/$", OauthQQUserView.as_view(), name="qq_user")
]
