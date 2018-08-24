from rest_framework.response import Response
from rest_framework.views import APIView

from oauth.utils import link_tx


class OauthQQView(APIView):
    """创建qq连接视图"""

    @staticmethod
    def get(request):
        # 将qq的url发给用户, 实现三方登陆
        url = link_tx.join_url("get_qq_code_id")
        return link_tx.send_url(url)


class OauthQQUserView(APIView):
    """与qq服务器交互"""

    @staticmethod
    def get(request):
        # 1. 从客户端拿到code
        code = request.query_params.get("code")

        # 2. 利用code访问qq获取token
        token_data = link_tx.get_url_data("get_qq_token", code)
        # 'callback( {"client_id":"101474184","openid":"3FCC18185E46F988D464CF0AC5CB9676"} );

        # 3. 利用token访问qq获取open_id
        open_id_data = link_tx.get_url_data("get_qq_open_id", token_data)

        openid = open_id_data.get("openid")
        print(openid)

        return Response(openid)


class WeChatView(APIView):
    """获取微信接口"""

    @staticmethod
    def get(request):
        """拼接url发给客户端实现三方登陆"""
        url = link_tx.join_url("get_wx_code_id")
        return link_tx.send_url(url)


class WeChatUserView(APIView):
    """与微信服务器交互"""

    @staticmethod
    def get(request):
        code = request.query_params.get("code")

        get_token_url = link_tx.get_url_data("get_wx_token")
        pass
