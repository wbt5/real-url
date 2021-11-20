# 小米直播：https://live.wali.com/fe

import requests


class WaLi:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        zuid = self.rid.split('_')[0]
        with requests.Session() as s:
            res = s.get(f'https://s.zb.mi.com/get_liveinfo?lid={self.rid}&zuid={zuid}').json()
        status = res['data']['status']
        if status == 1:
            flv = res['data']['video']['flv']
            return flv.replace('http', 'https')
        else:
            raise Exception('直播间不存在或未开播')


def get_real_url(rid):
    try:
        wali = WaLi(rid)
        return wali.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入小米直播房间号：\n')
    print(get_real_url(r))
