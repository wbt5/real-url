# 热猫直播：https://zhibo.yuanbobo.com/
import requests
import re


class YuanBoBo:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        with requests.Session() as s:
            res = s.get('https://zhibo.yuanbobo.com/' + str(self.rid)).text
        stream_id = re.search(r"stream_id:\s+'(\d+)'", res)
        if stream_id:
            status = re.search(r"status:\s+'(\d)'", res).group(1)
            if status == '1':
                real_url = 'http://ks-hlslive.yuanbobo.com/live/{}/index.m3u8'.format(stream_id.group(1))
                return real_url
            else:
                raise Exception('未开播')
        else:
            raise Exception('直播间不存在')


def get_real_url(rid):
    try:
        th = YuanBoBo(rid)
        return th.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('输入热猫直播房间号：\n')
    print(get_real_url(r))
