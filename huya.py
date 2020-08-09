# 获取虎牙直播的真实流媒体地址。
# 虎牙"一起看"频道的直播间可能会卡顿
import requests
import re
import base64
import urllib.parse
import hashlib
import time


def live(e):
    i, b = e.split('?')
    r = i.split('/')
    s = re.sub(r'.(flv|m3u8)', '', r[-1])
    c = b.split('&', 3)
    c = [i for i in c if i != '']
    n = {i.split('=')[0]: i.split('=')[1] for i in c}
    fm = urllib.parse.unquote(n['fm'])
    u = base64.b64decode(fm).decode('utf-8')
    p = u.split('_')[0]
    f = str(int(time.time() * 1e7))
    ll = n['wsTime']
    t = '0'
    h = '_'.join([p, t, s, f, ll])
    m = hashlib.md5(h.encode('utf-8')).hexdigest()
    y = c[-1]
    url = "{}?wsSecret={}&wsTime={}&u={}&seqid={}&{}".format(i, m, ll, t, f, y)
    return url


def huya(room_id):
    try:
        room_url = 'https://m.huya.com/' + str(room_id)
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36 '
        }
        response = requests.get(url=room_url, headers=header).text
        livelineurl = re.findall(r'liveLineUrl = "([\s\S]*?)";', response)[0]
        if livelineurl:
            if 'replay' in livelineurl:
                return '直播录像：https:' + livelineurl
            else:
                s_url = live(livelineurl)
                b_url = live(livelineurl.replace('_2000', ''))
                real_url = {
                    '2000p': "https:" + s_url,
                    'BD': "https:" + b_url
                }
        else:
            real_url = '未开播或直播间不存在'
    except:
        real_url = '未开播或直播间不存在'
    return real_url


if __name__ == '__main__':
    rid = input('输入虎牙直播间号：\n')
    print(huya(rid))
