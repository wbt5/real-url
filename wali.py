# 小米直播：https://live.wali.com/fe
import requests


def wali(rid):
    zuid = rid.split('_')[0]
    with requests.Session() as s:
        res = s.get('https://s.zb.mi.com/get_liveinfo?lid={}&zuid={}'.format(rid, zuid)).json()
    status = res['data']['status']
    if status == 1:
        flv = res['data']['video']['flv']
        return flv.replace('http', 'https')
    else:
        raise Exception('直播间不存在或未开播')


if __name__ == '__main__':
    r = input('输入小米直播房间号：\n')
    print(wali(r))
