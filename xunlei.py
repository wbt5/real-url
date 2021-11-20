# 迅雷直播：https://live.xunlei.com/global/index.html?id=0

import requests
import hashlib
import time
from urllib.parse import urlencode


class XunLei:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        url = 'https://biz-live-ssl.xunlei.com//caller'
        headers = {
            'cookie': 'appid=1002'
        }
        _t = int(time.time() * 1000)
        u = '1002'
        f = '&*%$7987321GKwq'
        params = {
            '_t': _t,
            'a': 'play',
            'c': 'room',
            'hid': 'h5-e70560ea31cc17099395c15595bdcaa1',
            'uuid': self.rid,
        }
        data = urlencode(params)
        p = hashlib.md5(f'{u}{data}{f}'.encode('utf-8')).hexdigest()
        params['sign'] = p
        with requests.Session() as s:
            res = s.get(url, params=params, headers=headers).json()
        if res['result'] == 0:
            play_status = res['data']['play_status']
            if play_status == 1:
                real_url = res['data']['data']['stream_pull_https']
                return real_url
            else:
                raise Exception('未开播')
        else:
            raise Exception('直播间可能不存在')


def get_real_url(rid):
    try:
        xl = XunLei(rid)
        return xl.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入迅雷直播房间号：\n')
    print(get_real_url(r))
