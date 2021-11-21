# 获取来疯直播的真实流媒体地址。
# 来疯直播就是优酷直播的个人主播频道，不同于优酷直播下的轮播台和体育直播。
# 来疯直播间链接形式：https://v.laifeng.com/8032155

import requests
import re


class LaiFeng:

    def __init__(self, rid):
        """
        来疯直播
        Args:
            rid: 房间号
        """
        self.rid = rid
        self.s = requests.Session()

    def get_real_url(self):
        try:
            response_main = self.s.get(f'http://v.laifeng.com/{self.rid}/m').text
            stream_name = re.search(r"initAlias:'(.*)?'", response_main).group(1)
            real_url = {}
            for stream_format in ['HttpFlv', 'Hls']:
                request_url = f'https://lapi.lcloud.laifeng.com/Play?AppId=101&CallerVersion=2.0&StreamName' \
                              f'={stream_name}&Action=Schedule&Version=2.0&Format={stream_format}'
                response = self.s.get(request_url).json()
                real_url[stream_format] = response.get(stream_format)[0].get('Url')
        except Exception:
            raise Exception('该直播间不存在或未开播')
        return real_url


def get_real_url(rid):
    try:
        lf = LaiFeng(rid)
        return lf.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入来疯直播房间号：\n')
    print(get_real_url(r))
