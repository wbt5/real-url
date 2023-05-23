import re
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib import parse

import requests

DEBUG = True

headers = {
    'authority': 'v.douyin.com',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
}

url = input('请输入【抖音直播链接】或【19位room_id】或【网页端直播间链接】：')
if re.match(r'\d{19}', url):
    room_id = url

if 'live' in url:
    option = Options()
    option.add_argument('--headless')
    browser = webdriver.Chrome(options=option)
    browser.get(url)
    ps = browser.page_source
    ps_parsed = parse.unquote(ps)
    id_raw = ps_parsed.split('roomId')[1].split('id_str')[0]
    room_id = re.search(r'\d{19}', id_raw).group(0)


else:
    try:
        url = re.search(r'(https.*)', url).group(1)
        response = requests.head(url, headers=headers)
        url = response.headers['location']
        room_id = re.search(r'\d{19}', url).group(0)
    except Exception as e:
        if DEBUG:
            print(e)
        print('获取room_id失败')
        sys.exit(1)
print('room_id', room_id)

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
except Exception as e:
    if DEBUG:
        print(e)
    print('获取real url失败')
