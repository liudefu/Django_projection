import base64
import pickle

from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection

from carts.serializer import CartSerializer
from contents.datail.content import LIVE_SAVE


class CartsView(APIView):
    """购物车增删改查"""

    def is_login(self, request):
        try:
            user = None if request.user.is_authenticated else request.user
        except Exception:
            user = None
        return user

    def validate_obj(self, data):
        s = CartSerializer(data=data)
        s.is_valid(raise_exception=True)
        return s
    def get_data(self, s):
        sku_id = s.data.get("sku_id")
        count = s.data.get("count")
        selected = s.data.get("selected", None)
        return sku_id, count, selected

    def perform_authentication(self, request):
        """重写方法让签名过期和错误的数据进入视图函数"""
        pass

    def post(self, request):
        """
        添加数据
        post提交
        :param: id, count, selected
        """
        s = self.validate_obj(request.data)
        sku_id, count, selected = self.get_data(s)
        # 1. 登陆用户, 数据存储在redis中
        if self.is_login(request):
            # 1. 登陆用户使用redis存储
            cur = get_redis_connection("cart")
            # 2. 使用管道符
            p1 = cur.pipeline()
            # 3. 添加并且修改数据
            p1.hincrby("cart_%s" % request.user.id, sku_id, count)
            if selected:
                # 如果选中, 就将当前的商品id添加到列表中
                p1.add("cart_selected_%s" % request.user.id, sku_id)
            p1.execute()
            return Response(s.data)
        # 2. 未登录用户, 数据存储在cookie中
        cart_str = request.COOKIES.get("cart", None)
        # 1. 判断是否为空, 如果有数据需要解码
        cart_dict = pickle.loads(base64.b64decode(cart_str.encode())) if cart_str else {}
        # 2. 如果有相同的商品, 进行累加:
        if sku_id in cart_str:
            # 从cookie中取出count进行累加
            count_save = cart_dict.get("sku_id").get("count")
            count += count_save
        # 3. 重新配置数据
        cart_dict[sku_id] = {
            "count": count,
            "selected": selected
        }

        response = Response(s.data)
        # 4. 编码发送
        encode_cart = base64.b64encode(pickle.dumps(cart_dict)).decode()
        response.set_cookie("cart", encode_cart, LIVE_SAVE)

        return response

    def get(self, request):
        """
        获取购物车数据
        :param:
        """
        s = self.validate_obj(request.data)
        sku_id, count, selected = self.get_data(s)
        # 1. 判断用户是否登陆
        if self.is_login(request.user):
            # 1. 连接redis
            cur = get_redis_connection("cart")
            cart_byte = cur.hgetall("cart_%s" % request.user.id)
            # redis_selected_ids = cur.

        pass
    def put(self):
        pass

    def delete(self):
        pass
