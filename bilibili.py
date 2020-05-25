# 获取哔哩哔哩直播的真实流媒体地址。
# PC网页和手机APP端的qn=1是最高画质;qn取值0~4。
# 手机网页端的只找到一个值qn=0。

import requests
import re


def get_real_rid(rid):
    room_url = 'https://api.live.bilibili.com/room/v1/Room/room_init?id=' + str(rid)
    response = requests.get(url=room_url).json()
    data = response.get('data', 0)
    if data:
        live_status = data.get('live_status', 0)
        room_id = data.get('room_id', 0)
    else:
        live_status = room_id = 0
    return live_status, room_id


def get_real_url_flv(rid):
    room = get_real_rid(rid)
    live_status = room[0]
    room_id = room[1]
    qn = 1 # PC网页和手机APP端的qn=1是最高画质;qn取值0~4。
    if live_status:
        try:
            room_url = 'https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomPlayInfo?room_id={}&play_url=1&mask=1&qn={}&platform=web'.format(room_id, qn)
            response = requests.get(url=room_url).json()
            durl = response.get('data').get('play_url').get('durl', 0)
            real_url = durl[-1].get('url')
        except:
            real_url = '疑似部分国外IP无法GET到正确数据，待验证'
    else:
        real_url = '未开播或直播间不存在'
    return real_url


def get_real_url_hls(rid):
    room = get_real_rid(rid)
    live_status = room[0]
    room_id = room[1]
    qn = 0 # 手机网页端的只找到一个值qn=0。
    if live_status:
        try:
            room_url = 'https://api.live.bilibili.com/xlive/web-room/v1/playUrl/playUrl?cid={}&platform=h5&otype=json&quality={}'.format(room_id, qn)
            response = requests.get(url=room_url).json()
            durl = response.get('data').get('durl', 0)
            real_url = durl[-1].get('url')
        except:
            real_url = '疑似部分国外IP无法GET到正确数据，待验证'
    else:
        real_url = '未开播或直播间不存在'
    return real_url

rid = input('请输入bilibili房间号：\n')
real_url_flv = get_real_url_flv(rid)
# real_url_hls = get_real_url_hls(rid)
print('该直播间源地址为：')
print(real_url_flv)
# print(real_url_hls)
