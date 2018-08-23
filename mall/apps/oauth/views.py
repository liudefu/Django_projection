from rest_framework.response import Response
from rest_framework.views import APIView

from contents.login.qq import *
from oauth.utils import join_url, get_url_data


class OauthQQView(APIView):
    """创建qq连接视图"""

    @staticmethod
    def get(request):
        code_id = request.query_params.get("code")
        params_dict = {
            "response_type": "code",
            "client_id": QQ_APP_ID,
            "redirect_uri": QQ_REDIRECT_URL,
            "state": code_id,
            "scope": "get_user_info"
        }
        url = join_url(GET_CODE_ID_URL, params_dict)
        return Response({"auth_url": url})


class OauthQQUserView(APIView):
    """与qq服务器交互"""

    @staticmethod
    def get(request):
        code_id = request.query_params.get("code")
        params_dict = {
            "grant_type": "authorization_code",
            "client_id": QQ_APP_ID,
            "client_secret": QQ_APP_KEY,
            "code": code_id,
            "redirect_uri": QQ_REDIRECT_URL
        }

        token_url = join_url(GET_TOKEN_URL, params_dict)
        token_dict = get_url_data(token_url)

        access_token = {
            "access_token": token_dict.get("access_token")[0]
        }
        open_id_url = join_url(GET_OPEN_ID_URL, access_token)

        open_id_dict = get_url_data(open_id_url)
        openid = open_id_dict.get("openid")
        print(openid)

        return Response(openid)
    # 'callback( {"client_id":"101474184","openid":"3FCC18185E46F988D464CF0AC5CB9676"} );
