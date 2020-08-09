# 艺气山直播：http://www.173.com/room/category?categoryId=11
import requests


def _173(rid):
    params = 'roomId={}&format=m3u8'.format(rid)
    with requests.Session() as s:
        res = s.post('http://www.173.com/room/getVieoUrl', params=params).json()
    data = res['data']
    if data:
        status = data['status']
        if status == 2:
            return data['url']
        else:
            raise Exception('未开播')
    else:
        raise Exception('直播间不存在')


if __name__ == '__main__':
    r = input('输入艺气山直播房间号：\n')
    print(_173(r))
