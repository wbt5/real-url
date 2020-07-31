# 棉花糖直播：https://www.2cq.com/rank
import requests


def mht(rid):
    with requests.Session() as s:
        res = s.get('https://www.2cq.com/proxy/room/room/info?roomId={}&appId=1004'.format(rid))
    res = res.json()
    if res['status'] == 1:
        result = res['result']
        if result['liveState'] == 1:
            real_url = result['pullUrl']
            return real_url
        else:
            raise Exception('未开播')
    else:
        raise Exception('直播间可能不存在')


if __name__ == '__main__':
    r = input('输入棉花糖直播房间号：\n')
    print(mht(r))
