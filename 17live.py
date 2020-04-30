# 获取17直播的真实流媒体地址。
# 17直播间链接形式：https://17.live/live/276480

import requests


def get_real_url(rid):
    try:
        response = requests.post(url='https://api-dsa.17app.co/api/v1/lives/' + rid +'/viewers/alive', data='{"liveStreamID":rid}').json()
        real_url = response.get('rtmpUrls')[0].get('url')
    except:
        real_url = '该直播间不存在或未开播' 
    return real_url


rid = input('请输入17直播房间号：\n')
real_url = get_real_url(rid)
print('该直播间源地址为：')
print(real_url)
