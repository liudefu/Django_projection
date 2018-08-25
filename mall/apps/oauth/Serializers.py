# coding=utf-8
from rest_framework import serializers

from oauth.models import OAuthQQUser
from users.models import User
from utils.open_id import decode_open_id
from utils.serializer_token import to_serializer
from utils.set_token import make_token
from utils.validate_sms_code import validate_sms_code


class OAuthUserSerializers(serializers.Serializer):
    """qq绑定序列化器"""
    mobile = serializers.RegexField(label="手机号", regex=r"^1[356789]\d{9}$", allow_null=False, required=True)
    access_token = serializers.CharField(label="openid", write_only=True)
    sms_code = serializers.CharField(label="验证码", max_length=6, min_length=6, write_only=True)
    password = serializers.CharField(label="密码", min_length=8, max_length=21)

    def validate(self, data):
        """序列化验证"""
        # 首先拿到openid的数据
        openid = data.pop("access_token", None)
        sms_code_test = data.get("sms_code", None)
        mobile = data.get("mobile", None)
        password = data.get("password", None)

        if not all([openid, sms_code_test, mobile, password]):
            raise serializers.ValidationError("数据不全!")

        openid = decode_open_id(openid)
        if openid is None:
            raise serializers.ValidationError("token失效!")
        data["openid"] = openid

        try:
            user = User.objects.get(mobile=mobile)
            data["user"] = user
        except User.DoesNotExist:
            # 验证短信验证码
            validate_sms = validate_sms_code(sms_code_test, mobile)
            if validate_sms is not True:
                raise serializers.ValidationError(validate_sms)
            return data
        return data

    def create(self, data):
        # 删除sms_code, access_token
        print(data)
        user = data.get("user", None)
        if user is None:
            user = User.objects.create(
                username=data.get("mobile"),
                password=data.get("password"),
                mobile=data.get("mobile")
            )
            user.set_password(data.get("password"))
            user.save()

        # 解密openid并添加到data中

        OAuthQQUser.objects.create(
            user=user,
            openid=data.get("openid")
        )
        token = make_token(user)
        data = to_serializer(token, user)
        return data

    def update(self, instance, data):
        pass
