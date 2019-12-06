# 获取哔哩哔哩直播的真实流媒体地址。
# quality=4默认画质为原画


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


def get_real_url(rid):
    room = get_real_rid(rid)
    live_status = room[0]
    room_id = room[1]
    if live_status:
        try:
            room_url = 'https://api.live.bilibili.com/xlive/web-room/v1/index/getRoomPlayInfo?room_id={}&play_url=1&mask=1&qn=0&platform=web'.format(room_id)
            response = requests.get(url=room_url).json()
            durl = response.get('data').get('play_url').get('durl', 0)
            real_url = durl[-1].get('url')
        except:
            real_url = '疑似部分国外IP无法GET到正确数据，待验证'
    else:
        real_url = '未开播或直播间不存在'
    return real_url


rid = input('请输入bilibili房间号：\n')
real_url = get_real_url(rid)
print('该直播间源地址为：\n' + real_url)
