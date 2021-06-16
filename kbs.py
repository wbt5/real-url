# -*- coding: utf-8 -*-
# @Time: 2021/5/22 8:02
# @Project: real-url
# @Author: wbt5
# @Blog: https://wbt5.com

import hashlib
import time
from urllib.parse import parse_qsl, urlsplit

import requests


class KBS:
    """
    - 腾讯体育直播，看比赛频道 https://kbs.sports.qq.com/
    - 直播间地址类似：https://sports.qq.com/kbsweb/game.htm?mid=100006:2337840，需要其中的mid
    - 只能获取免费观看的直播间
    - 请求参数params中的defn：蓝光fhd、超清shd、高清hd、标清sd，未登陆时最高获取超清，蓝光需VIP。
    """

    def __init__(self, rid):
        var = dict(parse_qsl(urlsplit(rid).query))
        mid = var.get('mid')

        with requests.Session() as self.s:
            res = requests.get(f'https://matchweb.sports.qq.com/kbs/matchDetail?mid={mid}').json()
            self.vid = res['data']['liveId']
            self.livepid = res['data']['programId']

    def get_real_url(self):
        tt = int(time.time())
        week = int(time.strftime('%w'))
        s = ('06fc1464', '4244ce1b', '77de31c5', 'e0149fa2', '60394ced', '2da639f0', 'c2f0cf9f')
        ha = f'{s[week - 1]}{self.vid}{tt}*#06#40201'
        ckey = hashlib.md5(ha.encode('utf-8')).hexdigest()
        params = {
            'cmd': 2,
            'cnlid': self.vid,
            'pla': 0,
            'stream': 2,
            'system': 0,
            'appVer': '3.0.0.142',
            'encryptVer': f'7.{7 if week == 0 else week}',
            'qq': 0,
            'device': 'PC',
            'guid': 'f56776a1fa52e9c8c4987bfecfbf0503',
            'defn': 'shd',  # shd默认超清
            'host': 'qq.com',
            'livepid': self.livepid,
            'logintype': 1,
            'vip_status': 1,
            'livequeue': 1,
            'fntick': tt,
            'tm': tt,
            'sdtfrom': 1107,
            'platform': 40201,
            'cKey': ckey,
            'queueStatus': 0,
            'sphttps': 1,
            'authext': '{}',
            'auth_ext': '{}',
            'auth_from': 40001,
            # 'callback': 'txvlive_videoinfoget_2767135792',
        }
        res = self.s.get('https://infozb6.video.qq.com/', params=params).json()
        playurl = res.get('playurl', 0)
        if res['errinfo']:
            raise Exception('errinfo')
        else:
            return playurl


def get_real_url(rid):
    try:
        kbs = KBS(rid)
        return kbs.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入腾讯体育直播间地址：\n')
    print(get_real_url(r))
