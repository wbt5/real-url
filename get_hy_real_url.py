# 获取虎牙直播的真实流媒体地址。


import requests
import re


def get_real_url(rid):
    room_url = 'https://m.huya.com/' + str(rid)
    header = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36'
    }
    response = requests.get(url=room_url, headers=header)
    pattern = r"hasvedio: '([\s\S]*.m3u8)"
    result = re.findall(pattern, response.text, re.I)
    if result:
        real_url = result[0]
        real_url = re.sub(r'_\d{3,4}.m3u8', '.flv', result[0])
    else:
        real_url = '未开播或直播间不存在'
    return real_url


rid = input('请输入虎牙房间号：\n')
real_url = get_real_url(rid)
print('该直播间源地址为：\n' + real_url)
