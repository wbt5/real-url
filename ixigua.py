# 获取西瓜直播的真实流媒体地址。

import requests
import re


class IXiGua:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:83.0) Gecko/20100101 Firefox/83.0'
            }
            room_url = 'https://live.ixigua.com/' + str(self.rid)
            response = requests.get(url=room_url, headers=headers).text
            real_url = re.findall(r'playInfo":([\s\S]*?),"authStatus', response)[0]
            real_url = re.sub(r'\\u002F', '/', real_url)
        except:
            raise Exception('直播间不存在或未开播')
        return real_url


def get_real_url(rid):
    try:
        xg = IXiGua(rid)
        return xg.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入西瓜直播房间号：\n')
    print(get_real_url(r))
