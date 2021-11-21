# 企鹅体育：https://live.qq.com/directory/all

import requests
import re


class ESport:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        with requests.Session() as s:
            res = s.get(f'https://m.live.qq.com/{self.rid}')
        show_status = re.search(r'"show_status":"(\d)"', res.text)
        if show_status:
            if show_status.group(1) == '1':
                hls_url = re.search(r'"hls_url":"(.*)","use_p2p"', res.text).group(1)
                return hls_url
            else:
                raise Exception('未开播')
        else:
            raise Exception('直播间不存在')


def get_real_url(rid):
    try:
        es = ESport(rid)
        return es.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入企鹅体育直播房间号：\n')
    print(get_real_url(r))
