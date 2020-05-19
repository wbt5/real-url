# 获取火猫直播的真实流媒体地址,默认为最高画质.
# 获取的流媒体地址如:http://live-lx-hdl.huomaotv.cn/live/qvCESZ?t=1573928152&r=377789475848&stream=qvCESZ&rid=oubvc2y3v&token=44a7f115f0af496e268bcbb7cdbb63b1&url=http%3A%2F%2Flive-lx-hdl.huomaotv.cn%2Flive%2FqvCESZ&from=huomaoh5room
# 实际上使用http://live-lx-hdl.huomaotv.cn/live/qvCESZ?token=44a7f115f0af496e268bcbb7cdbb63b1,即可播放
# 链接中lx可替换cdn(lx,tx,ws,js,jd2等),媒体类型可为.flv或.m3u8,码率可为BL8M,BL4M,TD,BD,HD,SD


import requests
import time
import hashlib
import re


def get_time():
    tt = str(int((time.time() * 1000)))
    return tt


def get_videoids(rid):
    room_url = 'https://www.huomao.com/mobile/mob_live/' + str(rid)
    response = requests.get(url=room_url).text
    try:
        videoids = re.findall(r'var stream = "([\w\W]+?)";', response)[0]
    except:
        videoids = 0
    return videoids


def get_token(videoids, time):
    token = hashlib.md5((str(videoids) + 'huomaoh5room' + str(time) +
                         '6FE26D855E1AEAE090E243EB1AF73685').encode('utf-8')).hexdigest()
    return token


def get_real_url(rid):
    videoids = get_videoids(rid)
    if videoids:
        time = get_time()
        token = get_token(videoids, time)
        room_url = 'https://www.huomao.com/swf/live_data'
        post_data = {
            'cdns': 1,
            'streamtype': 'live',
            'VideoIDS': videoids,
            'from': 'huomaoh5room',
            'time': time,
            'token': token
        }
        response = requests.post(url=room_url, data=post_data).json()
        roomStatus = response.get('roomStatus', 0)
        if roomStatus == '1':
            real_url_flv = response.get('streamList')[-1].get('list')[0].get('url')
            real_url_m3u8 = response.get('streamList')[-1].get('list_hls')[0].get('url')
            real_url = [real_url_flv, real_url_m3u8.replace('_480', '')]
        else:
            real_url = '直播间未开播'
    else:
        real_url = '直播间不存在'
    return real_url


rid = input('请输入火猫直播房间号：\n')
real_url = get_real_url(rid)
print('该直播间源地址为：')
print(real_url)
