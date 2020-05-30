# 获取56千帆直播的真实流媒体地址。
# 千帆直播直播间链接形式：https://qf.56.com/520686

import requests
import re


def get_real_url(rid):
    try:
        response = requests.post(url='https://qf.56.com/' + rid).text
        real_url = re.findall(r"flvUrl:'(.*)\?wsSecret", response)
        real_url = real_url[0]
    except:
        real_url = '该直播间不存在或未开播' 
    return real_url


rid = input('请输入千帆直播房间号：\n')
real_url = get_real_url(rid)
print('该直播间源地址为：')
print(real_url)
