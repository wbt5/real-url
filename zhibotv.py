# -*- coding: utf-8 -*-
# @Time: 2021/5/13 20:27
# @Project: real-url
# @Author: wbt5
# @Blog: https://wbt5.com

import requests


class ZhiBotv:

    def __init__(self, rid):
        """
        中国体育&新传宽频，直播间地址如：https://v.zhibo.tv/10007
        Args:
            rid:房间号
        """
        self.rid = rid
        self.params = {
            'token': '',
            'roomId': self.rid,
            'angleId': '',
            'lineId': '',
            'definition': 'hd',
            'statistics': 'pc|web|1.0.0|0|0|0|local|5.0.1',
        }
        self.BASE_URL = 'https://rest.zhibo.tv/room/get-pull-stream-info-v430'
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/95.0.4638.69 Safari/537.36 ',
            'Referer': 'https://www.zhibo.tv/live/'
        }

    def get_real_url(self):
        """
        no streaming 没开播;
        non-existent rid 房间号不存在;
        :return: url
        """
        with requests.Session() as s:
            res = s.get(self.BASE_URL, params=self.params, headers=self.HEADERS).json()
            if 'hlsHUrl' in res['data']:
                url = res['data'].get('hlsHUrl')
                if url:
                    return url
                else:
                    raise Exception('no streaming')
            else:
                raise Exception('non-existent rid')


def get_real_url(rid):
    try:
        zbtv = ZhiBotv(rid)
        return zbtv.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入中国体育房间号：\n')
    print(get_real_url(r))
