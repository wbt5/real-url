# 获取NOW直播的真实流媒体地址。

import requests


class Now:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        try:
            room_url = f'https://now.qq.com/cgi-bin/now/web/room/get_live_room_url?room_id={self.rid}&platform=8'
            response = requests.get(url=room_url).json()
            result = response.get('result')
            real_url = {
                'raw_hls_url': result.get('raw_hls_url', 0),
                'raw_rtmp_url': result.get('raw_rtmp_url', 0),
                'raw_flv_url': result.get('raw_flv_url', 0)
            }
        except Exception:
            raise Exception('直播间不存在或未开播')
        return real_url


def get_real_url(rid):
    try:
        now = Now(rid)
        return now.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入NOW直播间号：\n')
    print(get_real_url(r))
