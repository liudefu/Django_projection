# coding=utf-8
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token

from users.views import *

urlpatterns = [
    url(r"^usernames/(?P<username>\w{5,20})/count/$", ValidateUser.UserNameValidate.as_view(), name="username"),
    url(r'^phones/(?P<mobile>1[345789]\d{9})/count/$', ValidateUser.MobileValidate.as_view(), name='phone_count'),
    url(r"^$", CreateUserAPIView.as_view(), name="create_user"),
    url(r'^auths/$', obtain_jwt_token, name='auths'),
    url(r'^infos/$', UserDetailView.as_view(), name='detail'),
    url(r'^emails/$',EmailView.as_view(),name='send_mail'),
    url(r'^emails/verification/$',VerificationEmailView.as_view(),name='emails_verification'),
]
