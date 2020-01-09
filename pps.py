# 获取PPS奇秀直播的真实流媒体地址。

import requests
import json
import re


def get_real_url(rid):
    try:
        response = requests.get('http://m-x.pps.tv/room/' + str(rid)).text
        anchor_id = re.findall(r'anchor_id":(\d*),"online_uid', response)[0]
        url = 'https://x.pps.tv/api/room/getStreamConfig'
        params = {
            "type_id": 1,
            "vid": 1,
            "anchor_id": anchor_id,
            }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url=url, data=json.dumps(params), headers=headers).json()
        if response.get('data'):
            real_url = response.get('data').get('flv')
        else:
            real_url = '未开播'
    except:
        real_url = '直播间不存在'
    return real_url


rid = input('请输入奇秀直播房间号：\n')
real_url = get_real_url(rid)
print('该直播间源地址为：')
print(real_url)
