# 羚萌直播：https://live.51lm.tv/programs/Hot

from urllib.parse import urlencode
import requests
import time
import hashlib


class LM:

    def __init__(self, rid):
        self.rid = rid
        self.BASE_URL = 'https://www.51lm.tv/live/room/info/basic'

    def get_real_url(self):
        roominfo = {'programId': self.rid}

        def g(d):
            return hashlib.md5(f'{d}#{urlencode(roominfo)}#Ogvbm2ZiKE'.encode('utf-8')).hexdigest()

        lminfo = {
            'h': int(time.time()) * 1000,
            'i': -246397986,
            'o': 'iphone',
            's': 'G_c17a64eff3f144a1a48d9f02e8d981c2',
            't': 'H',
            'v': '4.20.43',
            'w': 'a710244508d3cc14f50d24e9fecc496a'
        }
        u = g(urlencode(lminfo))
        lminfo = f'G={u}&{urlencode(lminfo)}'
        with requests.Session() as s:
            res = s.post(self.BASE_URL, json=roominfo, headers={'lminfo': lminfo}).json()
        code = res['code']
        if code == 200:
            status = res['data']['isLiving']
            if status == 'True':
                real_url = res['data']['playUrl']
                return real_url
            else:
                raise Exception('未开播')
        elif code == -1:
            raise Exception('输入错误')
        elif code == 1201:
            raise Exception('直播间不存在')


def get_real_url(rid):
    try:
        lm = LM(rid)
        return lm.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('输入羚萌直播房间号：\n')
    print(get_real_url(r))
