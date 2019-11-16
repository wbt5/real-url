# 获取战旗直播（战旗TV）的真实流媒体地址。
# 默认画质为超清


import requests


def get_real_url(rid):
    room_url = 'https://m.zhanqi.tv/api/static/v2.1/room/domain/' + str(rid) + '.json'
    try:
        response = requests.get(url=room_url).json()
        videoId = response.get('data').get('videoId')
        if videoId:
            real_url = 'https://dlhdl-cdn.zhanqi.tv/zqlive/' + str(videoId) + '.flv'
        else:
            real_url = '未开播'
    except:
        real_url = '直播间不存在'
    return real_url


rid = input('请输入战旗直播房间号：\n')
real_url = get_real_url(rid)
print('该直播间源地址为：\n' + real_url)
