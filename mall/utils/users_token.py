# coding=utf-8


def jwt_response_payload_handler(token, user=None, request=None):
    """自定义返回数据"""
    return {
        'token': token,
        'user_id': user.id,
        'username': user.username
    }