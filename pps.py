# 获取PPS奇秀直播的真实流媒体地址。

import requests
import re
import time


def get_real_url(rid):
    try:
        response = requests.get('http://m-x.pps.tv/room/' + str(rid)).text
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
        real_url = '直播间未开播或不存在'
    return real_url


rid = input('请输入奇秀直播房间号：\n')
real_url = get_real_url(rid)
print('该直播间源地址为：')
print(real_url)
