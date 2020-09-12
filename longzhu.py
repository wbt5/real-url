# 获取龙珠直播的真实流媒体地址，默认最高码率。

import requests
import re


class LongZhu:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        try:
            response = requests.get('http://m.longzhu.com/' + str(self.rid)).text
            roomId = re.findall(r'roomId = (\d*);', response)[0]
            response = requests.get('http://livestream.longzhu.com/live/getlivePlayurl?roomId={}&hostPullType=2&isAdvanced=true&playUrlsType=1'.format(roomId)).json()
            real_url = response.get('playLines')[0].get('urls')[-1].get('securityUrl')
        except:
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
