# -*- coding: utf-8 -*-
# @Time: 2021/8/15 16:00
# @Project: my-spiders
# @Author: wbt5
# @Blog: https://wbt5.com
# BIGO LIVE:https://www.bigo.tv/cn/

import requests


class Bigo:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        with requests.Session() as s:
            url = f'https://ta.bigo.tv/official_website/studio/getInternalStudioInfo'
            res = s.post(url, data={'siteId': self.rid}).json()
            hls_src = res['data']['hls_src']
            play_url = hls_src if hls_src else '不存在或未开播'
            return play_url


def get_real_url(rid):
    try:
        url = Bigo(rid)
        return url.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('输入bigo直播房间号：\n')
    print(get_real_url(r))
