# 艾米直播：https://www.imifun.com/

import requests
import re


class IMFun:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        with requests.Session() as s:
            res = s.get(f'https://www.imifun.com/{self.rid}').text
        roomid = re.search(r'mixPkPlayUrl ="rtmp://wsmd.happyia.com/ivp/(\d+-\d+)"', res).group(1)
        if roomid:
            status = re.search(r"isLive:(\d),", res).group(1)
            if status == '1':
                real_url = f'https://wsmd.happyia.com/ivp/{roomid}.flv'
                return real_url
            else:
                raise Exception('未开播')
        else:
            raise Exception('直播间不存在')


def get_real_url(rid):
    try:
        imf = IMFun(rid)
        return imf.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('输入艾米直播房间号：\n')
    print(get_real_url(r))
