# 获取映客直播的真实流媒体地址。


import requests


def get_real_url(rid):
    try:
        room_url = 'https://webapi.busi.inke.cn/web/live_share_pc?uid=' + str(rid)
        response = requests.get(url=room_url).json()
        record_url = response.get('data').get('file').get('record_url')
        stream_addr = response.get('data').get('live_addr')
        real_url = {
            'record_url': record_url,
            'stream_addr': stream_addr
        }
    except:
        real_url = '直播间不存在或未开播'
    return real_url


rid = input('请输入映客直播间uid：\n')
real_url = get_real_url(rid)
print('该直播源地址为：')
print(real_url)
