import re
import os
import sys
import time
import wget
import requests
from progressbar import ProgressBar, Percentage, Bar, Timer, ETA, FileTransferSpeed
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import unquote

#设置进度条
widgets = ['Progress: ', Percentage(), ' ', Bar('#'), ' ', Timer(), ' ', ETA(), ' ', FileTransferSpeed()]
progress = ProgressBar(widgets=widgets)


DEBUG = False

headers = {
    'authority': 'v.douyin.com',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
}

#url = input('请输入抖音直播链接或19位room_id：')
url = input('请输入网页版抖音直播房间url或19位room_id：')
if re.match(r'\d{19}', url):
    room_id = url

#else:
#    try:
#        url = re.search(r'(https.*)', url).group(1)
#        response = requests.head(url, headers=headers)
#        url = response.headers['location']
#        room_id = re.search(r'\d{19}', url).group(0)
#    except Exception as e:
#        if DEBUG:
#            print(e)
#        print('获取room_id失败')
#        sys.exit(1)
#print('room_id', room_id)

# 从live.douyin.com160465665562这种永久链接获取room_id
else:
    s_maxchiron = requests.Session()

    def get_Cookies(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4515.159 Safari/537.36'
        }
        session = requests.session()
        res = session.post(url,headers=headers)
        cookies = res.cookies.items()
        cookie = ''
        for name, value in cookies:
            cookie += '{0}={1};'.format(name, value)
        return cookie

    def find_id(str):
        splited = str.split('roomId":"')
        roomId_raw = splited[-1]
        roomId = ''
        for i in range(19):
            roomId += roomId_raw[i]
        return roomId

    try:
        cookie_maxchiron = get_Cookies(url)
    except Exception as e:
        if DEBUG:
            print(e)
        print('获取cookie失败')

    headers = {
        'authority': 'v.douyin.com',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
        'cookie': cookie_maxchiron
    }

    try:
        r_maxchiron = s_maxchiron.get(url, headers=headers)
    except Exception as e:
        if DEBUG:
            print(e)
        print('请求url失败')
    soup = BeautifulSoup(r_maxchiron.text, 'html.parser')
    soup_decode = unquote(str(soup))
    #print(soup_decode)
    room_id = find_id(soup_decode)
    print(room_id)

inter = input('请输入重连间隔（秒）默认10s：') or '10'
target = input('请输入目标文件夹(path)默认D盘根目录：') or 'D:\\'

while True:
    try:
        headers.update({
            'authority': 'webcast.amemv.com',
            'cookie': '_tea_utm_cache_1128={%22utm_source%22:%22copy%22%2C%22utm_medium%22:%22android%22%2C%22utm_campaign%22:%22client_share%22}',
        })

        params = (
            ('type_id', '0'),
            ('live_id', '1'),
            ('room_id', room_id),
            ('app_id', '1128'),
        )

        response = requests.get('https://webcast.amemv.com/webcast/room/reflow/info/', headers=headers, params=params).json()

        rtmp_pull_url = response['data']['room']['stream_url']['rtmp_pull_url']
        hls_pull_url = response['data']['room']['stream_url']['hls_pull_url']
        print(rtmp_pull_url)
        print(hls_pull_url)

        try:
            #wget.download(rtmp_pull_url, target, bar=wget.bar_adaptive)
            filename = str(datetime.now()).replace(' ', '_').replace(':', '_') + '.flv'
            #print(os.path.join(target, room_id))
            true_target = os.path.join(target, room_id)

            if os.path.exists(true_target) == False :
                os.mkdir(true_target)
                print('已创建：', true_target)
            else:
                print(true_target, '已存在。准备下载中...')
            for i in progress(range(500)):
                print(os.path.join(true_target, filename))
                wget.download(rtmp_pull_url, os.path.join(true_target, filename))

        except Exception as e:
            if DEBUG:
                print(e)
            print('wget下载失败')

    except Exception as e:
        if DEBUG:
            print(e)
        print('获取real url失败')

    print('正在重连......')
    time.sleep(int(inter))
