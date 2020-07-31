# 95秀：http://www.95.cn/
import requests
import re


def jwxiu(rid):
    with requests.Session() as s:
        res = s.get('http://www.95.cn/{}.html'.format(rid)).text
    try:
        uid = re.search(r'"uid":(\d+),', res).group(1)
        status = re.search(r'"is_offline":"(\d)"', res).group(1)
    except AttributeError:
        raise Exception('没有找到直播间')
    if status == '0':
        real_url = 'http://play.95xiu.com/app/{}.flv'.format(uid)
        return real_url
    else:
        raise Exception('未开播')


if __name__ == '__main__':
    r = input('输入95秀房间号：\n')
    print(jwxiu(r))
