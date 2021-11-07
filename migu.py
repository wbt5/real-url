# -*- coding: utf-8 -*-
# @Time: 2021/11/6 10:51
# @Project: real-url
# @Author: wbt5
# @Blog: https://wbt5.com

import requests
from urllib import parse


class MiGu:
    """
    获取咪咕体育直播的流媒体地址
    直播列表:https://www.miguvideo.com/mgs/website/prd/sportMatchDetail.html
    直播间地址形式:https://www.miguvideo.com/mgs/website/prd/sportLive.html?mgdbId=120000173758
    mgdbId 120000173758即为房间号
    """

    def __init__(self, rid, rate=3):
        """
        Args:
            rate:估计是清晰度，默认rate=3是高清
            rid:房间号，如 120000173758
        """
        self.rid = rid
        self.rate = rate

    def get_real_url(self):
        """
        先获取contId
        Returns:
            url
        """
        headers = {
            'appId': 'miguvideo',
            'clientId': '',
            'SDKCEId': '',
            'terminalId': 'www',
            'userId': '',
            'userToken': '',
            'X-UP-CLIENT-CHANNEL-ID': '',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/95.0.4638.69 Safari/537.36',
            'Referer': 'https://www.miguvideo.com/',
        }
        url = 'https://app-sc.miguvideo.com/vms-match/v3/staticcache/basic/basic-data/{}'.format(self.rid)

        with requests.Session() as session:
            res = session.get(url, headers=headers).json()
        try:
            contid = res['body']['pId']
            url = f'https://webapi.miguvideo.com/gateway/playurl/v3/play/playurl?contId={contid}&rateType={self.rate}'
            res = session.get(url, headers=headers).json()
            try:
                playurl = res['body']['urlInfo']['url']
                real_url = self.calcu(playurl)
                return real_url
            except KeyError:
                return '未获取到url,可能参数错误！'
        except KeyError:
            return '未获取到contId'

    @staticmethod
    def calcu(pre_url):
        """
        计算ddCalcu，原始过程在pcPlayer.js的9432行到9460行。
        这里直接用python代码还原，其实可以简化。
        Args:
            pre_url:playurl请求返回的url用来拼接计算ddCalcu

        Returns:
            real_url:添加ddCalcu后的播放地址
        """
        params = dict(parse.parse_qsl(pre_url.split('?')[-1]))
        t = 'eeeeeeeee'
        r = str(params['timestamp'])
        n = str(params['ProgramID'])
        a = params['Channel_ID']
        o = params['puData']
        # s = '2624'
        # js里是遍历s，这里直接写死
        u = t[2] or 'e'
        ll = r[6] or 't'
        c = n[2] or "c"
        f = a[len(a) - 4] or 'n'
        d = o
        h = []
        for p in range(0, int(len(d) / 2)):
            h.append(d[len(d) - p - 1])
            if p < len(d) - p - 1:
                h.append(o[p])
            x = {
                1: u,
                2: ll,
                3: c,
                4: f
            }
            h.append(x[p]) if p in [1, 2, 3, 4] else ''
        v = ''.join(h)
        real_url = pre_url + '&ddCalcu=' + v
        return real_url


def get_real_url(rid):
    try:
        mg = MiGu(rid)
        return mg.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    rr = input('请输入咪咕直播间号：\n')
    print(get_real_url(rr))
