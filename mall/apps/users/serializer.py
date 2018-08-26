# coding=utf-8
import re

from rest_framework import serializers

from celery_tasks.tasks.email_send import send_verify_email
from users.models import User
from utils.token_JWT import make_token
from utils.token_itsdangerous import token_encode
from utils.validate_sms_code import validate_sms_code


# noinspection SpellCheckingInspection
class UserSerializer(serializers.ModelSerializer):
    """用户表单序列化器"""
    allow = serializers.CharField(write_only=True, allow_blank=True)
    sms_code = serializers.CharField(max_length=6, min_length=6, write_only=True, allow_blank=True)
    password2 = serializers.CharField(min_length=8, max_length=21, write_only=True, allow_blank=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "mobile",
                  "password2", "allow", "sms_code",
                  "token", "id", "email_active")
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

        sms_validate = validate_sms_code(sms_code_test, mobile)
        if sms_validate is not True:
            raise serializers.ValidationError(sms_validate)

        return attrs

    def create(self, attrs):
        attrs.pop("password2")
        attrs.pop("allow")
        attrs.pop("sms_code")

        # attrs["password"] = "pbkdf2_sha256$36000$" + sha256(attrs["password"].encode()).hexdigest() + "="

        user = super().create(attrs)
        user.set_password(attrs["password"])
        user.save()

        # 给user制作token, 并赋值
        user.token = make_token(user)

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """个人中心序列化器"""

    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'email_active')


class EmailSerializer(serializers.ModelSerializer):
    """邮箱认证序列化器"""

    class Meta:
        model = User
        fields = ["email", "id"]
        extra_kwargs = {
            "email": {
                "required": True
            }
        }

    def update(self, obj, data):
        email = data.get("email")
        obj.email = email
        obj.save()
        token = token_encode({"id": obj.id, "email": email})
        send_verify_email.delay(email, token)
        print("邮件发送成功!")
        return obj
