# 获取虎牙直播的真实流媒体地址。
# 现在虎牙直播链接需要密钥和时间戳了


import requests
import re


def get_real_url(room_id):
    room_url = 'https://m.huya.com/' + str(room_id)
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/75.0.3770.100 Mobile Safari/537.36 '
    }
    response = requests.get(url=room_url, headers=header)
    pattern = r"src=\"([\s\S]*)\" data-setup"
    pattern2 = r"replay"  # 判断是否是回放
    result = re.findall(pattern, response.text, re.I)
    if re.search(pattern2, response.text):
        return result[0]
    if result:
        url = re.sub(r'_[\s\S]*.m3u8', '.m3u8', result[0])  # 修改了正则留下了密钥和时间戳
        url = re.sub(r'hw.hls', 'al.hls', url)  # 华为的源好像比阿里的卡
    else:
        url = '未开播或直播间不存在'
    return "https:" + url


rid = input('请输入虎牙房间号：\n')
real_url = get_real_url(rid)
print('该直播间源地址为：\n' + real_url)
