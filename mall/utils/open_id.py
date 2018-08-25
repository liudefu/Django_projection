# coding=utf-8
from itsdangerous import TimedJSONWebSignatureSerializer as Ser
import itsdangerous
from mall.settings import SECRET_KEY

# 实例化加密对象, 设置密钥和有效期

ser_openid = Ser(SECRET_KEY, expires_in=3600)


def encode_open_id(openid):
    """加密openid"""

    # 加密, 返回值为二进制, 需要解码
    bytes_data = ser_openid.dumps({"openid": openid})
    data = bytes_data.decode()

    # 数据加密成token返回
    return data


def decode_open_id(openid):
    """解密openid"""
    try:

        decode_openid = ser_openid.loads(openid).get("openid")

    except itsdangerous.BadData:
        return None

    return decode_openid
