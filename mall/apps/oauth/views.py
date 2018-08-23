import json
from urllib import parse
from urllib.parse import parse_qs
from urllib.request import urlopen


from rest_framework.response import Response
from rest_framework.views import APIView

from contents.login.qq import *


class OauthQQView(APIView):
    """创建qq连接视图"""

    @staticmethod
    def get(request):
        code_id = request.query_params.get("code")
        base_url = "https://graph.qq.com/oauth2.0/authorize?"
        params_dict = {
            "response_type": "code",
            "client_id": QQ_APP_ID,
            "redirect_uri": QQ_REDIRECT_URL,
            "state": code_id,
            "scope": "get_user_info"
        }
        url = base_url + parse.urlencode(params_dict)
        return Response({"auth_url": url})


class OauthQQUserView(APIView):
    """与qq浏览器交互"""

    @staticmethod
    def get(request):
        code = request.query_params.get("code")

        base_url = "https://graph.qq.com/oauth2.0/token?"
        params_dict = {
            "grant_type": "authorization_code",
            "client_id": QQ_APP_ID,
            "client_secret": QQ_APP_KEY,
            "code": code,
            "redirect_uri": QQ_REDIRECT_URL
        }

        url = base_url + parse.urlencode(params_dict)
        data = urlopen(url)
        print(data)
        token_str = data.read().decode()
        token_dict = parse_qs(token_str)

        base_url1 = "https://graph.qq.com/oauth2.0/me?access_token=%s" % token_dict.get("access_token")[0]
        open_data = urlopen(base_url1)
        print(open_data)
        open_str = open_data.read().decode()
        open_dict = json.loads(open_str[10:-4])
        openid = open_dict.get("openid")

        return openid
    # 'callback( {"client_id":"101474184","openid":"3FCC18185E46F988D464CF0AC5CB9676"} );
