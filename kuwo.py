# 酷我聚星直播：http://jx.kuwo.cn/

import requests
import re


class KuWo:

    def __init__(self, rid):
        self.rid = rid
        self.BASE_URL = 'https://jxm0.kuwo.cn/video/mo/live/pull/h5/v3/streamaddr'
        self.s = requests.Session()

    def get_real_url(self):
        res = self.s.get(f'https://jx.kuwo.cn/{self.rid}').text
        roomid = re.search(r"roomId: '(\d*)'", res)
        if roomid:
            self.rid = roomid.group(1)
        else:
            raise Exception('未开播或房间号错误')
        params = {
            'std_bid': 1,
            'roomId': self.rid,
            'platform': 405,
            'version': 1000,
            'streamType': '3-6',
            'liveType': 1,
            'ch': 'fx',
            'ua': 'fx-mobile-h5',
            'kugouId': 0,
            'layout': 1,
            'videoAppId': 10011,
        }
        res = self.s.get(self.BASE_URL, params=params).json()
        if res['data']['sid'] == -1:
            raise Exception('未开播或房间号错误')
        try:
            url = res['data']['horizontal'][0]['httpshls'][0]
        except (KeyError, IndexError):
            url = res['data']['vertical'][0]['httpshls'][0]
        return url


def get_real_url(rid):
    try:
        kw = KuWo(rid)
        return kw.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('输入酷我聚星直播房间号：\n')
    print(get_real_url(r))
