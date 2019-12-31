# 获取快手直播的真实流媒体地址，默认输出最高画质
# 2019年12月31日更新，headers中需要添加cookie，失效更换


import requests
import json
import re


def get_real_url(rid):
    try:
        url = 'https://live.kuaishou.com/u/' + str(rid)
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'cookie': 'did=web_8ad78a7e9b64441293b9f53788a41109'
        }
        response = requests.get(url, headers=headers).text
        pattern = r'{"liveStream":{"type":"json","json":{"liveStreamId":.*"playUrls":(.*),"coverUrl":'
        real_url = json.loads(re.findall(pattern, response)[0])[0]
    except:
        real_url = '该直播间不存在或未开播'
    return real_url


rid = input('请输入快手直播间ID：\n')
real_url = get_real_url(rid)
print('该直播源地址为：')
print(real_url)
