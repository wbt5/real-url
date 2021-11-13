# 获取PPS奇秀直播的真实流媒体地址。

import requests
import re
import time


class PPS:

    def __init__(self, rid):
        self.rid = rid
        self.BASE_URL = 'https://m-x.pps.tv/api/stream/getH5'
        self.s = requests.Session()

    def get_real_url(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                          'like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'Referer': 'https://m-x.pps.tv/'
        }
        tt = int(time.time() * 1000)
        try:
            res = self.s.get(f'https://m-x.pps.tv/room/{self.rid}', headers=headers).text
            anchor_id = re.findall(r'anchor_id":"(\d*)', res)[0]
            params = {
                'qd_tm': tt,
                'typeId': 1,
                'platform': 7,
                'vid': 0,
                'qd_vip': 0,
                'qd_uid': anchor_id,
                'qd_ip': '114.114.114.114',
                'qd_vipres': 0,
                'qd_src': 'h5_xiu',
                'qd_tvid': 0,
                'callback': '',
            }
            res = self.s.get(self.BASE_URL, headers=headers, params=params).text
            real_url = re.findall(r'"hls":"(.*)","rate_list', res)[0]
        except Exception:
            raise Exception('直播间不存在或未开播')
        return real_url


def get_real_url(rid):
    try:
        pps = PPS(rid)
        return pps.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入奇秀直播房间号：\n')
    print(get_real_url(r))
