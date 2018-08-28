# Create your views here.
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializer import UserSerializer, UserDetailSerializer, EmailSerializer
from utils.token_itsdangerous import token_decode
from .models import User


class ValidateUser(object):
    """User注册验证类"""

    # noinspection PyAbstractClass,PyMethodMayBeStatic,PyUnusedLocal
    class UserNameValidate(APIView):
        @staticmethod
        def get(request, username):
            user = User.objects.filter(username=username).count()
            user_dict = {
                "count": user,
                "username": username
            }
            return Response(user_dict)

    # noinspection PyAbstractClass,PyMethodMayBeStatic,PyUnusedLocal
    class MobileValidate(APIView):
        """校验手机号"""

        @staticmethod
        def get(request, mobile):
            mobile = User.objects.filter(mobile=mobile).count()
            context = {
                "count": mobile,
                "mobile": mobile
            }
            return Response(data=context)


class CreateUserAPIView(CreateAPIView):
    """验证并创建User用户信息"""
    serializer_class = UserSerializer


# 1 前端需要提供： 用户名, 两次密码, 手机号,  短信验证码, 是否同意用户协议
# 2 继承CreateAIPView
# 3 调用验证


# class UserDetailView(GenericAPIView):
#     """个人中心"""
#
#     permission_classes = [IsAuthenticated]
#
#     def get(self,request):
#
#         user = request.user
#
#         serializer = UserDetailSerializer(instance=user)
#
#         return Response(serializer.data)

class UserDetailView(RetrieveAPIView):
    """个人中心"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailSerializer

    def get_object(self):
        return self.request.user


class EmailView(UpdateAPIView):
    """邮箱验证激活url发送"""
    # 1. 前端提供: email
    # 2. 用户认证
    # 3. 使用序列化器进行数据验证与保存
    permission_classes = [IsAuthenticated]
    serializer_class = EmailSerializer

    def get_object(self):
        return self.request.user


# noinspection PyMethodMayBeStatic
class VerificationEmailView(APIView):
    """邮箱激活"""

    def get(self, request):
        token = request.query_params.get("token", None)
        if token is None:
            return Response({"message": "token is None"}, status=status.HTTP_400_BAD_REQUEST)

        token = token_decode(token)
        try:
            user = User.objects.get(id=token.get("id", None), email=token.get("email", None))
        except User.DoesNotExist:
            return Response({"message": "连接失效!"}, status=status.HTTP_400_BAD_REQUEST)

        user.email_active = True
        user.save()
        print("用户邮箱激活成功!")
        return Response({"message": "ok!"})
