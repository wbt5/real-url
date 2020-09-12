# 获取一直播的真实流媒体地址。

import requests
import re


class YiZhiBo:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        try:
            scid = re.findall(r'/l/(\S*).html', self.rid)[0]
            flvurl = 'http://alcdn.f01.xiaoka.tv/live/{}.flv'.format(scid)
            m3u8url = 'http://al01.alcdn.hls.xiaoka.tv/live/{}.m3u8'.format(scid)
            rtmpurl = 'rtmp://alcdn.r01.xiaoka.tv/live/live/{}'.format(scid)
            real_url = {
                'flvurl': flvurl,
                'm3u8url': m3u8url,
                'rtmpurl': rtmpurl
            }
        except:
            raise Exception('链接错误')
        return real_url

    def get_status(self):
        try:
            scid = re.findall(r'/l/(\S*).html', self.rid)[0]
            response = requests.get(
                url='https://m.yizhibo.com/www/live/get_live_video?scid=' + str(scid)).json()
            status_code = response.get('data').get('info').get('status')
            status = '直播中' if status_code == 10 else '未开播'
        except:
            raise Exception('链接错误')
        return status


def get_real_url(rid):
    try:
        yzb = YiZhiBo(rid)
        return yzb.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入一直播房间地址：\n')
    print(get_real_url(r))
