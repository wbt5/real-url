# 京东直播：https://h5.m.jd.com/dev/3pbY8ZuCx4ML99uttZKLHC2QcAMn/live.html?id=1807004&position=0
import requests
import json


def jd(rid):
    url = 'https://api.m.jd.com/client.action'
    params = {
        'functionId': 'liveDetail',
        'body': json.dumps({'id': rid, 'videoType': 1}, separators=(',', ':')),
        'client': 'wh5'
    }
    with requests.Session() as s:
        res = s.get(url, params=params).json()
    data = res.get('data', 0)
    if data:
        status = data['status']
        if status == 1:
            real_url = data['h5Pull']
            return real_url
        else:
            print('未开播')
            real_url = '回放：' + data.get('playBack').get('videoUrl', 0)
            return real_url
    else:
        raise Exception('直播间不存在')


if __name__ == '__main__':
    r = input('输入京东直播间id：\n')
    print(jd(r))
