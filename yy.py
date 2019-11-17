# 获取YY直播的真实流媒体地址。
# 默认画质为高清：1280*720


import requests
import re
import json


def get_real_url(rid):
    room_url = 'http://interface.yy.com/hls/new/get/{rid}/{rid}/1200?source=wapyy&callback=jsonp3'.format(rid=rid)
    headers = {
        'referer': 'http://wap.yy.com/mobileweb/{rid}'.format(rid=rid),
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }
    try:
        response = requests.get(url=room_url, headers=headers).text
        json_data = json.loads(re.findall(r'\(([\W\w]*)\)', response)[0])
        real_url = json_data.get('hls', 0)
        if not real_url:real_url='未开播或直播间不存在'
    except:
        real_url = '请求错误或直播间不存在'
    return real_url


rid = input('请输入YY直播房间号：\n')
real_url = get_real_url(rid)
print('该直播间源地址为：\n' + real_url)
