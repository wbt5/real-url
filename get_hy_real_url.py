import requests
import re


def get_real_url(rid):
    room_url = 'https://m.huya.com/' + rid
    header = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36'
    }
    response = requests.get(url=room_url, headers=header)
    pattern = r"hasvedio: '([\s\S]*.m3u8)"
    result = re.findall(pattern, response.text, re.I)
    real_url = result[0]
    return real_url


rid = input('请输入虎牙房间号：\n')
real_url = get_real_url(rid)
print('该直播间地址为：\n' + real_url)
