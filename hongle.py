# 红人直播：https://www.hongle.tv/
from urllib.parse import urlencode
import requests
import time
import hashlib


def hongle(rid):
    url = 'https://service.hongle.tv/v2/roomw/media'
    accesstoken = 'YeOucg9SmlbeeicDSN9k0efa4JaecMNbQd7eTQDNQRRmqUHnA%2Bwq4g%3D%3D'
    params = {
        '_st1': int(time.time() * 1000),
        'accessToken': accesstoken,
        'of': 1,
        'showid': rid,
        'tku': 44623062,
    }
    data = urlencode(params) + 'yuj1ah5o'
    _ajaxData1 = hashlib.md5(data.encode('utf-8')).hexdigest()
    params['_ajaxData1'] = _ajaxData1
    params['accessToken'] = 'YeOucg9SmlbeeicDSN9k0efa4JaecMNbQd7eTQDNQRRmqUHnA+wq4g=='
    with requests.Session() as s:
        res = s.get(url, params=params)
    if res.status_code == 200:
        res = res.json()
        statuscode = res['status']['statuscode']
        if statuscode == '0':
            if res['data']['live_status'] == '1':
                real_url = res['data']['media_url_web']
                real_url = real_url.replace('http', 'https')
                real_url = real_url.replace('__', '&')
                return real_url
            else:
                raise Exception('未开播')
        else:
            raise Exception('房间不存在')
    else:
        raise Exception('参数错误')


if __name__ == '__main__':
    r = input('输入红人直播房间号：\n')
    print(hongle(r))
