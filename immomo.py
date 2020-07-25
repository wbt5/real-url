import requests


def immomo(rid):
    url = 'https://web.immomo.com/webmomo/api/scene/profile/roominfos'
    data = {
        'stid': rid,
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


if __name__ == '__main__':
    r = input('输入陌陌直播房间号：\n')
    print(immomo(r))

# https://web.immomo.com/live/337033339
