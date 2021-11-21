# KK直播：http://www.kktv5.com/
import requests


class KK:

    def __init__(self, rid):
        """
        KK直播
        Args:
            rid: 房间号
        """
        self.rid = rid
        self.s = requests.Session()

    def get_real_url(self):
        url = 'https://sapi.kktv1.com/meShow/entrance?parameter={}'
        parameter = {'FuncTag': 10005043, 'userId': f'{self.rid}', 'platform': 1, 'a': 1, 'c': 100101}
        res = self.s.get(url.format(parameter)).json()
        tagcode = res['TagCode']
        if tagcode == '00000000':
            if res.get('liveType', 0) == 1:
                roomid = res['roomId']
                parameter = {'FuncTag': 60001002, 'roomId': roomid, 'platform': 1, 'a': 1, 'c': 100101}
                res = self.s.get(url.format(parameter)).json()
                real_url = res['liveStream']
                return real_url
            else:
                raise Exception('未开播')
        else:
            raise Exception('直播间不存在')


def get_real_url(rid):
    try:
        kk = KK(rid)
        return kk.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('输入KK直播房间号：\n')
    print(get_real_url(r))
