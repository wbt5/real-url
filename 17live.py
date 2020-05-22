# 获取17直播的真实流媒体地址。
# 17直播间链接形式：https://17.live/live/276480

import requests


def get_real_url(rid):
    try:
        response = requests.get(url='https://api-dsa.17app.co/api/v1/lives/' + rid).json()
        real_url_default = response.get('rtmpUrls')[0].get('url')
        userID = response.get('userID', 0)
        real_url_wansu = ''
        if userID:
            real_url_wansu = 'http://wansu-china-pull-rtmp-17.tigafocus.com/vod/' + userID + '.flv'
        real_url = [real_url_default, real_url_wansu]
    except:
        real_url = '该直播间不存在或未开播' 
    return real_url


rid = input('请输入17直播房间号：\n')
real_url = get_real_url(rid)
print('该直播间源地址为：')
print(real_url)
