# 九秀直播：https://www.9xiu.com/other/classify?tag=all&index=all

import requests


class JXiu:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        with requests.Session() as s:
            url = f'https://h5.9xiu.com/room/live/enterRoom?rid={self.rid}'
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) '
                              'AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
            }
            res = s.get(url, headers=headers).json()
        if res['code'] == 200:
            status = res['data']['status']
            if status == 0:
                raise Exception('未开播')
            elif status == 1:
                live_url = res['data']['live_url']
                return live_url
        else:
            raise Exception('直播间可能不存在')


def get_real_url(rid):
    try:
        jx = JXiu(rid)
        return jx.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('输入九秀直播房间号：\n')
    print(get_real_url(r))
