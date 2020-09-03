# 获取17直播的真实流媒体地址。
# 17直播间链接形式：https://17.live/live/276480

import requests


class Live17:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        try:
            response = requests.get(url='https://api-dsa.17app.co/api/v1/lives/' + self.rid).json()
            real_url_default = response.get('rtmpUrls')[0].get('url')
            real_url_modify = real_url_default.replace('global-pull-rtmp.17app.co', 'china-pull-rtmp-17.tigafocus.com')
            real_url = [real_url_modify, real_url_default]
        except:
            raise Exception('直播间不存在或未开播')
        return real_url


def get_real_url(rid):
    try:
        live17 = Live17(rid)
        return live17.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入17直播房间号：\n')
    print(get_real_url(r))
