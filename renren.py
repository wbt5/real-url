# 人人直播：http://zhibo.renren.com/

import requests
import re
import hashlib


class RenRen:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        with requests.Session() as s:
            res = s.get('http://activity.renren.com/liveroom/' + str(self.rid))
        livestate = re.search(r'"liveState":(\d)', res.text)
        if livestate:
            try:
                s = re.search(r'"playUrl":"([\s\S]*?)"', res.text).group(1)
                if livestate.group(1) == '0':
                    # accesskey = re.search(r'accesskey=(\w+)', s).group(1)
                    # expire = re.search(r'expire=(\d+)', s).group(1)
                    # live = re.search(r'(/live/\d+)', s).group(1)
                    # c = accesskey + expire + live
                    # key = hashlib.md5(c.encode('utf-8')).hexdigest()
                    # e = s.split('?')[0].split('/')[4]
                    # t = 'http://ksy-hls.renren.com/live/' + e + '/index.m3u8?key=' + key
                    return s
                elif livestate.group(1) == '1':
                    return '回放：' + s
            except IndexError:
                raise Exception('解析错误')
        else:
            raise Exception('直播间不存在')


def get_real_url(rid):
    try:
        rr = RenRen(rid)
        return rr.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入人人直播房间号：\n')
    print(get_real_url(r))
