# coding=utf-8
import re

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """用户表单序列化器"""
    allow = serializers.CharField(write_only=True, allow_blank=True)
    sms_code = serializers.CharField(max_length=6, min_length=6, write_only=True, allow_blank=True)
    password2 = serializers.CharField(min_length=8, max_length=21, write_only=True, allow_blank=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "mobile",
                  "password2", "allow", "sms_code", "token", "id")
        extra_kwargs = {
            "id": {"read_only": True},
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

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
        cur.delete("sms_code_%s" % mobile)
        if not sms_code:
            raise serializers.ValidationError("验证码过期")
        if sms_code.decode() != sms_code_test:
            raise serializers.ValidationError("验证码输入错误！")
        return attrs

    def create(self, attrs):
        attrs.pop("password2")
        attrs.pop("allow")
        attrs.pop("sms_code")

        # attrs["password"] = "pbkdf2_sha256$36000$" + sha256(attrs["password"].encode()).hexdigest() + "="

        user = super().create(attrs)
        user.set_password(attrs["password"])
        user.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token

        return user
