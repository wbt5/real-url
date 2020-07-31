# 酷我聚星直播：http://jx.kuwo.cn/
import requests


def kuwo(rid):
    with requests.Session() as s:
        res = s.get('https://zhiboserver.kuwo.cn/proxy.p?src=h5&cmd=enterroom&rid={}&videotype=1&auto=1'.format(rid))
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


if __name__ == '__main__':
    r = input('输入酷我聚星直播房间号：\n')
    print(kuwo(r))
