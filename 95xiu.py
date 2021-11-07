# 95秀：http://www.95.cn/

import requests
import re


class JWXiu:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        with requests.Session() as s:
            res = s.get(f'https://www.95.cn/{self.rid}.html').text
        try:
            uid = re.search(r'"uid":(\d+),', res).group(1)
            status = re.search(r'"is_offline":"(\d)"', res).group(1)
        except AttributeError:
            raise Exception('没有找到直播间')
        if status == '0':
            real_url = f'https://play1.95xiu.com/app/{uid}.flv'
            return real_url
        else:
            raise Exception('未开播')


def get_real_url(rid):
    try:
        jwx = JWXiu(rid)
        return jwx.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('输入95秀房间号：\n')
    print(get_real_url(r))
