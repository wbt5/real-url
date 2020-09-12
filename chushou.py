# 获取触手直播的真实流媒体地址。

import requests


class ChuShou:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        try:
            room_url = 'https://chushou.tv/h5player/video/get-play-url.htm?roomId={}&protocols=2&callback='.format(self.rid)
            response = requests.get(url=room_url).json()
            data = response.get('data')[0]
            real_url = {
                'sdPlayUrl': data.get('sdPlayUrl', 0),
                'hdPlayUrl': data.get('hdPlayUrl', 0),
                'shdPlayUrl': data.get('shdPlayUrl', 0)
            }
        except:
            raise Exception('直播间不存在或未开播')
        return real_url


def get_real_url(rid):
    try:
        cs = ChuShou(rid)
        return cs.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入触手直播房间号：\n')
    print(get_real_url(r))

