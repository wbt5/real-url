# 获取战旗直播（战旗TV）的真实流媒体地址。https://www.zhanqi.tv/lives
# 默认最高画质

import json
import re

import requests


class ZhanQi:

    def __init__(self, rid):
        """
        战旗直播间有两种：一种是普通直播间号为数字或字幕；另一种是官方的主题直播间，链接带topic。
        所以先判断一次后从网页源代码里获取数字直播间号
        Args:
            rid:直播间链接，从网页源码里获取真实数字rid
        """
        self.s = requests.Session()
        res = self.s.get(rid).text
        self.rid = re.search(r'"code":"(\d+)"', res).group(1)

    def get_real_url(self):
        res = self.s.get(f'https://m.zhanqi.tv/api/static/v2.1/room/domain/{self.rid}.json')
        try:
            res = res.json()
            videoid = res['data']['videoId']
            status = res['data']['status']
        except (KeyError, json.decoder.JSONDecodeError):
            raise Exception('Incorrect rid')

        if status == '4':
            # 获取gid
            res = self.s.get('https://www.zhanqi.tv/api/public/room.viewer')
            try:
                res = res.json()
                gid = res['data']['gid']
            except KeyError:
                raise Exception('Getting gid incorrectly')

            # 获取cdn_host
            res = self.s.get('https://umc.danuoyi.alicdn.com/dns_resolve_https?app=zqlive&host_key=alhdl-cdn.zhanqi.tv')
            cdn_host, *_ = res.json().get('redirect_domain')

            # 获取chain_key
            data = {
                'stream': f'{videoid}.flv',
                'cdnKey': 202,
                'platform': 128,
            }
            headers = {
                'cookie': f'gid={gid}',
            }
            res = self.s.post('https://www.zhanqi.tv/api/public/burglar/chain', data=data, headers=headers).json()
            chain_key = res['data']['key']
            url = f'https://{cdn_host}/alhdl-cdn.zhanqi.tv/zqlive/{videoid}.flv?{chain_key}&playNum=68072487067' \
                  f'&gId={gid}&ipFrom=1&clientIp=&fhost=h5&platform=128'
            return url
        else:
            raise Exception('No streaming')


def get_real_url(rid):
    try:
        zq = ZhanQi(rid)
        return zq.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    # 直播间链接类似：https://www.zhanqi.tv/topic/owl 或 https://www.zhanqi.tv/152600919
    r = input('输入战旗直播间的链接：\n')
    print(get_real_url(r))
