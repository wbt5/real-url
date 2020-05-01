# 获取来疯直播的真实流媒体地址。
# 来疯直播就是优酷直播的个人主播频道，不同于优酷直播下的轮播台和体育直播。
# 来疯直播间链接形式：https://v.laifeng.com/8032155

import requests
import re


def get_real_url(rid):
    try:
        response_main = requests.get(url='http://v.laifeng.com/{}/m'.format(rid)).text
        stream_name = re.findall(r"initAlias:'(.*)?'", response_main)[0]
        real_url = {}
        for stream_format in ['HttpFlv', 'Hls']:
            request_url = 'https://lapi.lcloud.laifeng.com/Play?AppId=101&StreamName={}&Action=Schedule&Version=2.0&Format={}'.format(stream_name, stream_format)
            response = requests.get(url=request_url).json()
            real_url[stream_format] = response.get(stream_format)[0].get('Url')
    except:
        real_url = '该直播间不存在或未开播'
    return real_url


rid = input('请输入来疯直播房间号：\n')
real_url = get_real_url(rid)
print('该直播间源地址为：')
print(real_url)
