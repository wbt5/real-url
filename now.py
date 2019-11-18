# 获取NOW直播的真实流媒体地址。


import requests


def get_real_url(rid):
    try:
        room_url = 'https://now.qq.com/cgi-bin/now/web/room/get_live_room_url?room_id={}&platform=8'.format(rid)
        response = requests.get(url=room_url).json()
        result = response.get('result')
        real_url = {
            'raw_hls_url': result.get('raw_hls_url', 0),
            'raw_rtmp_url': result.get('raw_rtmp_url', 0),
            'raw_flv_url': result.get('raw_flv_url', 0)
        }
    except:
        real_url = '直播间不存在或未开播'
    return real_url


rid = input('请输入NOW直播间数字ID：\n')
real_url = get_real_url(rid)
print('该直播源地址为：')
print(real_url)
