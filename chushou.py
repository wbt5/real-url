# 获取触手直播的真实流媒体地址。


import requests


def get_real_url(rid):
    try:
        room_url = 'https://chushou.tv/h5player/video/get-play-url.htm?roomId={}&protocols=2&callback='.format(rid)
        response = requests.get(url=room_url).json()
        data = response.get('data')[0]
        real_url = {
            'sdPlayUrl': data.get('sdPlayUrl', 0),
            'hdPlayUrl': data.get('hdPlayUrl', 0),
            'shdPlayUrl': data.get('shdPlayUrl', 0)
        }
    except:
        real_url = '直播间不存在或未开播'
    return real_url


rid = input('请输入触手直播间数字ID：\n')
real_url = get_real_url(rid)
print('该直播源地址为：')
print(real_url)
