# 获取花椒直播的真实流媒体地址。

import requests
import time


class HuaJiao:

    def __init__(self, rid):
        self.rid = rid
        self.headers = {
            'Referer': 'https://h.huajiao.com/l/index?liveid={}&qd=hu'.format(rid)
        }

    def get_real_url(self):
        tt = str(time.time())
        try:
            room_url = 'https://h.huajiao.com/api/getFeedInfo?sid={tt}&liveid={rid}'.format(tt=tt, rid=self.rid)
            response = requests.get(url=room_url, headers=self.headers).json()
            real_url = response.get('data').get('live').get('main')
        except:
            raise Exception('直播间不存在或未开播')
        return real_url


def get_real_url(rid):
    try:
        hj = HuaJiao(rid)
        return hj.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入花椒直播房间号：\n')
    print(get_real_url(r))
