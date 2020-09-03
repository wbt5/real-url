import requests


class ImMoMo:
    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        url = 'https://web.immomo.com/webmomo/api/scene/profile/roominfos'
        data = {
            'stid': self.rid,
            'src': 'url'
        }

        with requests.Session() as s:
            s.get('https://web.immomo.com')
            res = s.post(url, data=data).json()

        ec = res.get('ec', 0)
        if ec != 200:
            raise Exception('请求参数错误')
        else:
            live = res['data']['live']
            if live:
                real_url = res['data']['url']
                return real_url
            else:
                raise Exception('未开播')


def get_real_url(rid):
    try:
        mm = ImMoMo(rid)
        return mm.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入陌陌直播房间号：\n')
    print(get_real_url(r))

