# 获取快手直播的真实流媒体地址，默认输出最高画质

import requests
import json
import re


def get_real_url(rid):
    try:
        room_url = 'https://m.gifshow.com/fw/live/' + str(rid)
        headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'cookie': 'did=web_'}
        response = requests.get(url=room_url, headers=headers).text
        m3u8_url = re.findall(r'type="application/x-mpegURL" src="([\s\S]*?)_sd1000(tp)?(/index)?.m3u8', response)[0]
        real_url = [m3u8_url[0] + i for i in ['.flv', '.m3u8']]
    except:
        real_url = '该直播间不存在或未开播'
    return real_url


rid = input('请输入快手直播间ID：\n')
real_url = get_real_url(rid)
print('该直播源地址为：')
print(real_url)
