# 获取酷狗繁星直播的真实流媒体地址，默认最高码率。

import requests


def get_real_url(rid):
    try:
        response = requests.get('https://fx1.service.kugou.com/video/pc/live/pull/v3/streamaddr?roomId={}&ch=fx&version=1.0&streamType=1-2-5&platform=7&ua=fx-flash&kugouId=0&layout=1'.format(rid)).json()
        real_url = response.get('data').get('horizontal')[0].get('httpflv')
    except:
        real_url = '直播间不存在或未开播'
    return real_url


rid = input('请输入龙珠直播房间号：\n')
real_url = get_real_url(rid)
print('该直播间源地址为：')
print(real_url)
