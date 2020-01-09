# 获取六间房直播的真实流媒体地址。

import requests
import re


def get_real_url(rid):
    try:
        response = requests.get('https://v.6.cn/' + str(rid)).text
        result = re.findall(r'"flvtitle":"v(\d*?)-(\d*?)"', response)[0]
        uid = result[0]
        flvtitle = 'v{}-{}'.format(*result)
        response = requests.get('https://rio.6rooms.com/live/?s=' + str(uid)).text
        hip = 'https://' + re.findall(r'<watchip>(.*\.xiu123\.cn).*</watchip>', response)[0]
        real_url = [hip + '/' + flvtitle + '/playlist.m3u8', hip + '/httpflv/' + flvtitle]
    except:
        real_url = '直播间不存在或未开播'
    return real_url


rid = input('请输入六间房直播ID：\n')
real_url = get_real_url(rid)
print('该直播间源地址为：')
print(real_url)
