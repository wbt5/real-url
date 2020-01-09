# 获取龙珠直播的真实流媒体地址，默认最高码率。

import requests
import re


def get_real_url(rid):
    try:
        response = requests.get('http://m.longzhu.com/' + str(rid)).text
        roomId = re.findall(r'roomId = (\d*);', response)[0]
        response = requests.get('http://livestream.longzhu.com/live/getlivePlayurl?roomId={}&hostPullType=2&isAdvanced=true&playUrlsType=1'.format(roomId)).json()
        real_url = response.get('playLines')[0].get('urls')[-1].get('securityUrl')
    except:
        real_url = '直播间不存在或未开播'
    return real_url


rid = input('请输入龙珠直播房间号：\n')
real_url = get_real_url(rid)
print('该直播间源地址为：')
print(real_url)
