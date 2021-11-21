# 获取酷狗繁星直播的真实流媒体地址，默认最高码率。

import requests


class KuGou:

    def __init__(self, rid):
        """
        酷狗繁星直播
        Args:
            rid: 房间号
        """
        self.rid = rid
        self.s = requests.Session()
        self.BASE_URL = 'https://fx1.service.kugou.com/video/mo/live/pull/h5/v3/streamaddr'

    def get_real_url(self):
        params = {
            'roomId': self.rid,
            'platform': 18,
            'version': 1000,
            'streamType': '3-6',
            'liveType': 1,
            'ch': 'fx',
            'ua': 'fx-mobile-h5',
            'kugouId': 0,
            'layout': 1
        }
        try:
            res = self.s.get(self.BASE_URL, params=params).json()
            if res['code'] == 1:
                raise Exception(f'{res["msg"]}，可能是房间号输入错误！')
            real_url_hls = res.get('data').get('horizontal')[0].get('httpshls')[0]
        except IndexError:
            try:
                url = f'https://fx1.service.kugou.com/biz/ChannelVServices/' \
                      f'RoomLiveService.RoomLiveService.getCurrentLiveStarForMob/{self.rid}'
                res = self.s.get(url).json()
                if res['code'] == 1:
                    raise Exception(f'{res["msg"]}，可能是房间号输入错误！')
                roomid = res['data']['roomId']
                self.BASE_URL = 'https://fx2.service.kugou.com/video/pc/live/pull/mutiline/streamaddr'
                params = {
                    'std_rid': roomid,
                    'version': '1.0',
                    'streamType': '1-2-3-5-6',
                    'targetLiveTypes': '1-4-5-6',
                    'ua': 'fx-h5'
                }
                res = self.s.get(self.BASE_URL, params=params).json()
                real_url_hls = res.get('data').get('lines')[-1].get('streamProfiles')[-1]['httpsHls'][-1]
            except Exception:
                raise Exception('未找到')
        return real_url_hls


def get_real_url(rid):
    try:
        kg = KuGou(rid)
        return kg.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入酷狗直播房间号：\n')
    print(get_real_url(r))
