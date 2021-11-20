# 获取YY直播的真实流媒体地址。https://www.yy.com/1349606469
# 默认获取最高画质

import requests
import re
import json


class YY:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        headers = {
            'referer': f'https://wap.yy.com/mobileweb/{self.rid}',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/95.0.4638.69 Safari/537.36 '
        }
        room_url = f'https://interface.yy.com/hls/new/get/{self.rid}/{self.rid}/1200?source=wapyy&callback='
        with requests.Session() as s:
            res = s.get(room_url, headers=headers)
        if res.status_code == 200:
            data = json.loads(res.text[1:-1])
            if data.get('hls', 0):
                xa = data['audio']
                xv = data['video']
                xv = re.sub(r'_0_\d+_0', '_0_0_0', xv)
                url = f'https://interface.yy.com/hls/get/stream/15013/{xv}/15013/{xa}?source=h5player&type=m3u8'
                res = s.get(url).json()
                real_url = res['hls']
                return real_url
            else:
                raise Exception('未开播')
        else:
            raise Exception('直播间不存在')


def get_real_url(rid):
    try:
        yy = YY(rid)
        return yy.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('输入YY直播房间号：\n')
    print(get_real_url(r))
