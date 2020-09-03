# 获取PPS奇秀直播的真实流媒体地址。

import requests
import re
import time


class PPS:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        try:
            response = requests.get('http://m-x.pps.tv/room/' + str(self.rid)).text
            anchor_id = re.findall(r'anchor_id":(\d*),"online_uid', response)[0]
            tt = int(time.time() * 1000)
            url = 'http://api-live.iqiyi.com/stream/geth5?qd_tm={}&typeId=1&platform=7&vid=0&qd_vip=0&qd_uid={}&qd_ip=114.114.114.114&qd_vipres=0&qd_src=h5_xiu&qd_tvid=0&callback='.format(tt, anchor_id)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': 'http://m-x.pps.tv/'
            }
            response = requests.get(url=url, headers=headers).text
            real_url = re.findall(r'"hls":"(.*)","rate_list', response)[0]
        except:
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
