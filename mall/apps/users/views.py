# Create your views here.
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from areas.serializer import AddressTitleSerializer
from users.serializer import UserSerializer, UserDetailSerializer, EmailSerializer, AddressSerializer
from utils.token_itsdangerous import token_decode
from verifications import serializer
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


class AddressViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    """收货人地址视图"""
    # 1. 添加retrieve
    # 2. 删除Destroy
    # 3. 修改update
    # 4. 查询list
    # 5. 权限校验
    # 6. 只显示没有删除的
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        """获取查询集"""
        return self.request.user.addresses.filter(is_delete=0)

    def create(self, request, *args, **kwargs):
        """创建"""
        count = request.user.addresses.count()
        if count >= 10:
            return Response({'message': '保存地址数量已经达到上限'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        address = self.get_object()
        address.is_deleted = 1
        address.save()
        return Response({"message": "delete success"}, status=200)

    def update(self, request, *args, **kwargs):
        address = self.get_object()
        address.save_dict(request.query_params)
        address.save()
        return Response({"message": "update success"})

    def list(self, request, *args, **kwargs):
        """
        获取用户地址列表
        """
        # 获取所有地址
        queryset = self.get_queryset()
        # 创建序列化器
        serializer = self.get_serializer(queryset, many=True)
        user = self.request.user
        # 响应
        return Response({
            'user_id': user.id,
            'default_address_id': user.default_address_id,
            'limit': 20,
            'addresses': serializer.data,
        })

    @action(methods=['put'], detail=True)
    def title(self, request, pk=None, address_id=None):
        """
        修改标题
        """
        address = self.get_object()
        serializer = AddressTitleSerializer(instance=address, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=['put'], detail=True)
    def status(self, request, pk=None, address_id=None):
        """
        设置默认地址
        """
        address = self.get_object()
        request.user.default_address = address
        request.user.save()
        return Response({'message': 'OK'}, status=status.HTTP_200_OK)
