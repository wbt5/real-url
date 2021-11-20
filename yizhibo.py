# 获取一直播的真实流媒体地址。

import requests
import re


class YiZhiBo:

    def __init__(self, rid):
        """
        一直播需要传入直播间的完整地址
        Args:
            rid:完整地址
        """
        self.rid = rid
        self.s = requests.Session()

    def get_real_url(self):
        try:
            res = self.s.get(self.rid).text
            play_url, status_code = re.findall(r'play_url:"(.*?)"[\s\S]*status:(\d+),', res)[0]
            if status_code == '10':
                return play_url
            else:
                raise Exception('未开播')
        except Exception:
            raise Exception('获取错误')


def get_real_url(rid):
    try:
        yzb = YiZhiBo(rid)
        return yzb.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入一直播房间地址：\n')
    print(get_real_url(r))
