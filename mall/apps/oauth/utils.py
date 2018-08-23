# coding=utf-8
from urllib import parse


def join_url(base_url, params_dict):
    """将base_url与字典拼接成url参数传递"""
    return base_url + parse.urlencode(params_dict)


def get_url_data(url):
    """获取url数据"""
    import json
    from urllib.request import urlopen
    from urllib.parse import parse_qs

    data_bytes = urlopen(url)
    data_str = data_bytes.read().decode()
    data_dict = parse_qs(data_str)or json.loads(data_str[10:-4])

    return data_dict
