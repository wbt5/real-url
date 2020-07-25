# 获取斗鱼直播间的真实流媒体地址，可在PotPlayer、flv.js等播放器中播放。
# 2019年11月2日：修复斗鱼预览地址获取的方法；新增未开播房间的判断。
# 2019年12月4日：斗鱼更新后更简单了，可直接在播放页源码的JS中找到播放地址。


import requests
import re
import execjs
import time
import hashlib


def get_tt():
    tt1 = str(int(time.time()))
    tt2 = str(int((time.time() * 1000)))
    today = time.strftime('%Y%m%d', time.localtime())
    return tt1, tt2, today


def get_homejs(rid):
    room_url = 'https://m.douyu.com/' + rid
    response = requests.get(url=room_url)
    pattern_real_rid = r'"rid":(\d{1,7})'
    real_rid = re.findall(pattern_real_rid, response.text, re.I)[0]
    if real_rid != rid:
        room_url = 'https://m.douyu.com/' + real_rid
        response = requests.get(url=room_url)
    homejs = ''
    pattern = r'(function ub9.*)[\s\S](var.*)'
    result = re.findall(pattern, response.text, re.I)
    str1 = re.sub(r'eval.*;}', 'strc;}', result[0][0])
    homejs = str1 + result[0][1]
    return homejs, real_rid


def get_sign(rid, post_v, tt, ub9):
    docjs = execjs.compile(ub9)
    res2 = docjs.call('ub98484234')
    str3 = re.sub(r'\(function[\s\S]*toString\(\)', '\'', res2)
    md5rb = hashlib.md5((rid + '10000000000000000000000000001501' + tt + '2501' +
                         post_v).encode('utf-8')).hexdigest()
    str4 = 'function get_sign(){var rb=\'' + md5rb + str3
    str5 = re.sub(r'return rt;}[\s\S]*','return re;};', str4) 
    str6 = re.sub(r'"v=.*&sign="\+', '', str5)
    docjs1 = execjs.compile(str6)
    sign = docjs1.call(
        'get_sign', rid, '10000000000000000000000000001501', tt)
    return sign


def mix_room(rid):
    result1 = 'PKing'
    return result1


def get_pre_url(rid, tt):
    request_url = 'https://playweb.douyucdn.cn/lapi/live/hlsH5Preview/' + rid
    post_data = {
        'rid': rid,
        'did': '10000000000000000000000000001501'
    }
    auth = hashlib.md5((rid + str(tt)).encode('utf-8')).hexdigest()
    header = {
        'content-type': 'application/x-www-form-urlencoded',
        'rid': rid,
        'time': tt,
        'auth': auth
    }
    response = requests.post(url=request_url, headers=header, data=post_data)
    response = response.json()
    pre_url = ''
    if response.get('error') == 0:
        real_url = (response.get('data')).get('rtmp_live')
        if 'mix=1' in real_url:
            pre_url = mix_room(rid)
        else:
            pattern1 = r'^[0-9a-zA-Z]*'
            pre_url = re.search(pattern1, real_url, re.I).group()
    return pre_url


def get_sign_url(post_v, rid, tt, ub9):
    sign = get_sign(rid, post_v, tt, ub9)
    request_url = 'https://m.douyu.com/api/room/ratestream'
    post_data = {
        'v': '2501' + post_v,
        'did': '10000000000000000000000000001501',
        'tt': tt,
        'sign': sign,
        'ver': '219032101',
        'rid': rid,
        'rate': '-1'
    }
    header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36'
    }
    response = requests.post(url=request_url, headers=header, data=post_data).json()
    if response.get('code') == 0:
        real_url = (response.get('data')).get('url')
        if 'mix=1' in real_url:
            result1 = mix_room(rid)
        else:
            pattern = r'/(\d{1,8}[0-9a-zA-Z]+)_?[\d]{0,4}.m3u8'
            result1 = re.search(pattern, real_url).group(1)
    else:
        result1 = 0
    return result1


def get_real_url(rid):
    rid = str(rid)
    tt = get_tt()
    url = get_pre_url(rid, tt[1])
    if url:
        return "http://tx2play1.douyucdn.cn/live/" + url + ".flv?uuid="
    else:
        result = get_homejs(rid)
        real_rid = result[1]
        homejs = result[0]
        real_url = get_sign_url(tt[2], real_rid, tt[0], homejs)
        if real_url != 0:
            real_url = "http://tx2play1.douyucdn.cn/live/" + real_url + ".flv?uuid="
        else:
            real_url = '未开播'
        return real_url


def get_url_from_js(rid):
    # 从播放页源代码中直接匹配地址
    header = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    try:
        response = requests.get('https://www.douyu.com/{}'.format(rid), headers=header).text
        real_url = re.findall(r'live/({}[\d\w]*?)_'.format(rid), response)[0]
    except:
        real_url = '直播间未开播或不存在'
    return "http://tx2play1.douyucdn.cn/live/" + real_url + ".flv?uuid="


rid = input('请输入斗鱼数字房间号：\n')
real_url = get_real_url(rid)
print('该直播间地址为：\n' + real_url)

# print(get_url_from_js('85894'))