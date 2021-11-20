# 人人直播：http://zhibo.renren.com/

import requests
import re


class RenRen:

    def __init__(self, rid):
        """
        直播间地址形式：http://activity.renren.com/live/liveroom/970302934_21348
        rid即970302934_21348
        Args:
            rid:房间号
        """
        self.rid = rid
        self.s = requests.Session()

    def get_real_url(self):
        res = self.s.get(f'http://activity.renren.com/live/liveroom/{self.rid}').text
        try:
            s = re.search(r'playUrl":"(.*?)"', res)
            play_url = s.group(1)
            return play_url
        except Exception:
            raise Exception('解析错误')


def get_real_url(rid):
    try:
        rr = RenRen(rid)
        return rr.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入人人直播房间号：\n')
    print(get_real_url(r))
