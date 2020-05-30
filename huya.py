# 获取虎牙直播的真实流媒体地址。
# 现在虎牙直播链接需要密钥和时间戳了


import requests
import re


def get_real_url(room_id):
    try:
        room_url = 'https://m.huya.com/' + str(room_id)
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/75.0.3770.100 Mobile Safari/537.36 '
        }
        response = requests.get(url=room_url, headers=header).text
        liveLineUrl = re.findall(r'liveLineUrl = "([\s\S]*?)";', response)[0]
        if liveLineUrl:
            if 'replay' in liveLineUrl:
                return '直播录像：' + liveLineUrl
            else:
                real_url = ["https:" + re.sub(r'_\d{4}.m3u8', '.m3u8', liveLineUrl), "https:" + liveLineUrl]
        else:
            real_url = '未开播或直播间不存在'
    except:
        real_url = '未开播或直播间不存在'
    return real_url


rid = input('请输入虎牙房间号：\n')
real_url = get_real_url(rid)
print('该直播间源地址为：')
print(real_url)