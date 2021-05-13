# -*- coding: utf-8 -*-
# @Time: 2021/5/13 20:27
# @Project: real-url
# @Author: wbt5
# @Blog: https://wbt5.com

import requests


class ZhiBotv:

    def __init__(self, rid):
        self.rid = rid
        self.params = {

            'token': '',
            'roomId': self.rid,
            'angleId': '',
            'lineId': '',
            'definition': 'hd',
            'statistics': 'pc|web|1.0.0|0|0|0|local|5.0.1',

        }

    def get_real_url(self):
        """
        no streaming 没开播;
        non-existent rid 房间号不存在;
        :return: url
        """
        with requests.Session() as s:
            res = s.get('https://rest.zhibo.tv/room/get-pull-stream-info-v430', params=self.params).json()
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
