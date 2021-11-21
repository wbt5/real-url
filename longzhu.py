# 获取龙珠直播的真实流媒体地址，默认最高码率。

import requests
import re


class LongZhu:

    def __init__(self, rid):
        """
        龙珠直播，获取hls格式的播放地址
        Args:
            rid: 直播房间号
        """
        self.rid = rid
        self.s = requests.Session()

    def get_real_url(self):
        try:
            res = self.s.get(f'http://star.longzhu.com/{self.rid}').text
            roomId = re.search(r'roomid":(\d+)', res).group(1)
            res = self.s.get(f'http://livestream.longzhu.com/live/getlivePlayurl?roomId={roomId}&utmSr=&platform=h5'
                             f'&device=ios').json()
            real_url = res.get('playLines')[0].get('urls')[-1].get('securityUrl')
        except Exception:
            raise Exception('直播间不存在或未开播')
        return real_url


def get_real_url(rid):
    try:
        lz = LongZhu(rid)
        return lz.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入龙珠直播房间号：\n')
    print(get_real_url(r))
