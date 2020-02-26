# 获取一直播的真实流媒体地址。


import requests
import re


def get_real_url(room_url):
    try:
        scid = re.findall(r'/l/(\S*).html', room_url)[0]
        flvurl = 'http://alcdn.f01.xiaoka.tv/live/{}.flv'.format(scid)
        m3u8url = 'http://al01.alcdn.hls.xiaoka.tv/live/{}.m3u8'.format(scid)
        rtmpurl = 'rtmp://alcdn.r01.xiaoka.tv/live/live/{}'.format(scid)
        real_url = {
            'flvurl': flvurl,
            'm3u8url': m3u8url,
            'rtmpurl': rtmpurl
        }
    except:
        real_url = '链接错误'
    return real_url


def get_status(room_url):
    try:
        scid = re.findall(r'/l/(\S*).html', room_url)[0]
        response = requests.get(
            url='https://m.yizhibo.com/www/live/get_live_video?scid=' + str(scid)).json()
        status_code = response.get('data').get('info').get('status')
        status = '直播中' if status_code == 10 else '未开播'
    except:
        status = '链接错误'
    return status


rid = input('请输入一直播房间地址：\n')
status = get_status(rid)
print('当前直播状态', status)
real_url = get_real_url(rid)
print('该直播间源地址为：')
print(real_url)
