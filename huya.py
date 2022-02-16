# 获取虎牙直播的真实流媒体地址。

import requests
import re
import base64
import urllib.parse
import hashlib
import time
import random
import hashlib


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
    f = str(int(time.time() * 1e7))
    l = n['wsTime']
    mt = n['txyp']
    t = str(random.randint(1460000000000, 1650000000000))
    mm = t+f
    ml = n['ctype']
    fs = n['fs']
    sp = n['sphdcdn']
    spp = n['sphdDC']
    spd = n['sphd']
    ll = mm+'|'+ml+'|103'
    ms = hashlib.md5(ll.encode("utf-8")).hexdigest()
    h = '_'.join([p, t, s, ms, l])
    m = hashlib.md5(h.encode('utf-8')).hexdigest()
    urls = "{}?wsSecret={}&wsTime={}&seqid={}&ctype={}&ver=1&txyp={}&fs={}&&sphdcdn={}&sphdDC={}&sphd={}&t=103&ratio=0&u={}&t=103&sv=2110211124".format(i, m, l, mm, ml, mt, fs, sp, spp, spd, t)
    aa, ab = urls.split('//')
    url = 'https://'+ab
    return url


def get_real_url(room_id):
    room_url = 'https://mp.huya.com/cache.php?m=Live&do=profileRoom&roomid=' + str(room_id)
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/75.0.3770.100 Mobile Safari/537.36 '
    }
    data = requests.get(url=room_url, headers=header).json()
    liveline = data['data']['stream']['flv']['multiLine'][2]['url']
    liveline = live(liveline)
    return liveline
rid = input('输入虎牙直播房间号：\n')
real_url = get_real_url(rid)
print('该直播间源地址为：')
print(real_url)
