# 获取56千帆直播的真实流媒体地址。
# 千帆直播直播间链接形式：https://qf.56.com/520686

import requests
import re


class QF:

    def __init__(self, rid):
        """
        搜狐千帆直播可以直接在网页源码里找到播放地址
        Args:
            rid: 数字直播间号
        """
        self.rid = rid
        self.s = requests.Session()

    def get_real_url(self):
        try:
            res = self.s.get(f'https://qf.56.com/{self.rid}').text
            flvurl = re.search(r"flvUrl:'(.*)?'", res).group(1)
            if 'flv' in flvurl:
                real_url = flvurl
            else:
                res = self.s.get(flvurl).json()
                real_url = res['url']
        except Exception:
            raise Exception('直播间不存在或未开播')
        return real_url


def get_real_url(rid):
    try:
        qf = QF(rid)
        return qf.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入千帆直播房间号：\n')
    print(get_real_url(r))
