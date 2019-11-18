# 获取西瓜直播的真实流媒体地址。


import requests
import re
import json

def get_real_url(rid):
    try:
        room_url = rid
        response = requests.get(url=room_url).text
        real_url = re.findall(r'playInfo":([\s\S]*?),"authStatus', response)[0]
        real_url = re.sub(r'\\u002F', '/', real_url)
    except:
        real_url = '直播间不存在或未开播'
    return real_url


rid = input('请输入西瓜直播URL：\n')
real_url = get_real_url(rid)
print('该直播源地址为：')
print(real_url)
