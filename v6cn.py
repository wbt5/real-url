# 获取六间房直播的真实流媒体地址。

import requests
import re


class V6CN:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        try:
            response = requests.get(f'https://v.6.cn/{self.rid}').text
            result = re.findall(r'"flvtitle":"v(\d*?)-(\d*?)"', response)[0]
            uid = result[0]
            flvtitle = 'v{}-{}'.format(*result)
            response = requests.get(f'https://rio.6rooms.com/live/?s={uid}').text
            hip = 'https://' + re.search(r'<watchip>(.*\.com).*?</watchip>', response).group(1)
            real_url = [f'{hip}/{flvtitle}/palylist.m3u8', f'{hip}/httpflv/{flvtitle}']
        except Exception:
            raise Exception('直播间不存在或未开播')
        return real_url


def get_real_url(rid):
    try:
        v6cn = V6CN(rid)
        return v6cn.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入六间房直播房间号：\n')
    print(get_real_url(r))
