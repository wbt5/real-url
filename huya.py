# 获取虎牙直播的真实流媒体地址。
# 虎牙"一起看"频道的直播间可能会卡顿，尝试将返回地址 tx.hls.huya.com 中的 tx 改为 bd、migu-bd。

import requests
import re
import base64
import urllib.parse
import hashlib
import time


class HuYa:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        try:
            room_url = 'https://m.huya.com/' + str(self.rid)
            header = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36 '
            }
            response = requests.get(url=room_url, headers=header).text
            livelineurl = re.findall(r'liveLineUrl = "([\s\S]*?)";', response)[0]
            livelineurl = base64.b64decode(livelineurl).decode('utf-8')
            if livelineurl:
                if 'replay' in livelineurl:
                    real_url = {
                        'replay': "https:" + livelineurl,
                    }
                else:
                    stream_name = self.get_stream_name(livelineurl)
                    base_url = 'http://121.12.115.15/tx.hls.huya.com/src/' + stream_name
                    real_url = {
                        'hls': base_url + '.m3u8',
                        'flv': base_url + '.flv',
                        'hls_2m': base_url + '.m3u8?ratio=2000',
                        'flv_2m': base_url + '.flv?ratio=2000'
                    }
            else:
                raise Exception('未开播或直播间不存在')
        except Exception as e:
            raise Exception('未开播或直播间不存在')
        return real_url

    @staticmethod
    def get_stream_name(e):
        i, b = e.split('?')
        r = i.split('/')
        s = re.sub(r'.(flv|m3u8)', '', r[-1])
        return s

    @staticmethod
    def live(e):
        i, b = e.split('?')
        r = i.split('/')
        s = re.sub(r'.(flv|m3u8)', '', r[-1])
        c = b.split('&')
        c = [i for i in c if i != '']
        n = {i.split('=')[0]: i.split('=')[1] for i in c}
        fm = urllib.parse.unquote(n['fm'])
        u = base64.b64decode(fm).decode('utf-8')
        p = u.split('_')[0]
        seqid = str(int(time.time() * 1e7))
        ctype = n['ctype']
        t = n['t']
        mf = hashlib.md5((seqid + '|' + ctype + '|' + t).encode('utf-8')).hexdigest()
        ll = n['wsTime']
        ratio = n.get('ratio')
        if ratio is None:
            ratio = ''
        uid = '1279523789849'
        h = '_'.join([p, uid, s, mf, ll])
        m = hashlib.md5(h.encode('utf-8')).hexdigest()
        txyp = n['txyp']
        fs = n['fs']
        url = "{}?wsSecret={}&wsTime={}&uuid=&uid={}&seqid={}&ratio={}&txyp={}&fs={}&ctype={}&ver=1&t={}".format(
            i, m, ll, uid, seqid, ratio, txyp, fs, ctype, t)
        return url


def get_real_url(rid):
    try:
        hy = HuYa(rid)
        return hy.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    rid = input('输入虎牙直播房间号：\n')
    print(get_real_url(rid))
