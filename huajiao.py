# 获取花椒直播的真实流媒体地址。


import requests
import time


def get_real_url(rid):
    tt = str(time.time())
    try:
        room_url = 'https://h.huajiao.com/api/getFeedInfo?sid={tt}&liveid={rid}'.format(tt=tt, rid=rid)
        response = requests.get(url=room_url).json()
        real_url = response.get('data').get('live').get('main')
    except:
        real_url = '直播间不存在或未开播'
    return real_url


rid = input('请输入花椒直播间号：\n')
real_url = get_real_url(rid)
print('该直播源地址为：\n' + real_url)
