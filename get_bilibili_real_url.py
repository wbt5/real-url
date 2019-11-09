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
        room_url = 'https://api.live.bilibili.com/room/v1/Room/playUrl?cid=' +str(room_id) + '&platform=h5&otype=json&quality=4'
        response = requests.get(url=room_url).json()
        result = response.get('data').get('durl')[0].get('url')
        pattern = r'.com/live-[\S]*/([\s\S]*.m3u8)'
        pattern_result = re.findall(pattern, result, re.I)[0]
        real_url = 'https://cn-hbxy-cmcc-live-01.live-play.acgvideo.com/live-bvc/' + pattern_result
    else:
        real_url = '未开播或直播间不存在'
    return real_url


rid = input('请输入bilibili房间号：\n')
real_url = get_real_url(rid)
print('该直播间源地址为：\n' + real_url)
