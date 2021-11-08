# 艺气山直播：http://www.173.com/room/category?categoryId=11

import requests


class YQS:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        params = f'roomId={self.rid}'
        with requests.Session() as s:
            res = s.post('https://www.173.com/room/getVieoUrl', params=params).json()
        data = res['data']
        if data:
            status = data['status']
            if status == 2:
                return data['url']
            else:
                raise Exception('未开播')
        else:
            raise Exception('直播间不存在')


def get_real_url(rid):
    try:
        yqs = YQS(rid)
        return yqs.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('输入艺气山直播房间号：\n')
    print(get_real_url(r))
