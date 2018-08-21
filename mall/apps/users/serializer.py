# coding=utf-8
import re

from django_redis import get_redis_connection
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    # allow = serializers.CharField(allow_null=False,allow_blank=False,write_only=True)
    # sms_code = serializers.CharField(max_length=6, min_length=6, allow_null=False,allow_blank=False,write_only=True)
    # password2 = serializers.CharField(min_length=8, max_length=21, allow_null=True, write_only=True)
    allow = serializers.CharField(write_only=True)
    sms_code = serializers.CharField(max_length=6, min_length=6, write_only=True)
    password2 = serializers.CharField(min_length=8, max_length=21, write_only=True)
    class Meta:
        model = User
        write_only_fields = ("allow", "sms_code", "password2")
        fields = ("username", "password", "mobile",
                  "date_joined", "last_login", "password2",
                  "allow", "sms_code")
        ex

    def validate(self, attrs):
        password1 = attrs.get("password")
        password2 = attrs.get("password2")
        mobile = attrs.get("mobile")
        allow = attrs.get("allow")
        sms_code_test = attrs.get("sms_code")
        if password1 != password2:
            raise serializers.ValidationError("两次输入密码不一致！")
        if not re.match(r"^1[356789]\d{9}$", mobile):
            raise serializers.ValidationError("手机号不合法！")
        if not allow:
            raise serializers.ValidationError("请勾选用户协议！")
        cur = get_redis_connection("code")
        sms_code = cur.get("sms_code_%s" % mobile)
        # cur.delete("sms_code_%s" % mobile)
        if not sms_code:
            raise serializers.ValidationError("验证码过期")
        if sms_code.decode() != sms_code_test:
            raise serializers.ValidationError("验证码输入错误！")
        return attrs

    def create(self, attrs):
        attrs.pop("password2")
        attrs.pop("allow")
        attrs.pop("sms_code")
        user = super().create(attrs)
        return user
