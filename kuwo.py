# 酷我聚星直播：http://jx.kuwo.cn/

import requests


class KuWo:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        with requests.Session() as s:
            res = s.get('https://zhiboserver.kuwo.cn/proxy.p?src=h5&cmd=enterroom&rid={}&videotype=1&auto=1'.format(self.rid))
        res = res.json()
        try:
            livestatus = res['room']['livestatus']
        except KeyError:
            raise Exception('房间号错误')
        if livestatus == 2:
            real_url = res['live']['url']
            return real_url
        else:
            raise Exception('未开播')


def get_real_url(rid):
    try:
        kw = KuWo(rid)
        return kw.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('输入酷我聚星直播房间号：\n')
    print(get_real_url(r))

