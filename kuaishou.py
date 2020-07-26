# 获取快手直播的真实流媒体地址，全部都要

import requests
import json
import re

def get_standard_url(response):
    try:
        m3u8_url = re.findall(r'"STANDARD":"([\s\S]*?)"},', response)[0]
        flv_url = re.findall(r'"name":"STANDARD","shortName":"STANDARD",[\s\S]*?,"url":"([\s\S]*?)","', response)[0]
        print('标清：', [m3u8_url, flv_url])
    except:
        print('无法获取标清地址')

def get_high_url(response):
    try:
        m3u8_url = re.findall(r'"HIGH":"([\s\S]*?)"},', response)[0]
        flv_url = re.findall(r'"name":"HIGH","shortName":"HIGH",[\s\S]*?,"url":"([\s\S]*?)","', response)[0]
        print('高清：', [m3u8_url, flv_url])
    except:
        print('无法获取高清地址')

def get_super_url(response):
    try:
        m3u8_url = re.findall(r'"SUPER":"([\s\S]*?)"},', response)[0]
        flv_url = re.findall(r'"name":"SUPER","shortName":"SUPER",[\s\S]*?,"url":"([\s\S]*?)","', response)[0]
        print('蓝光：', [m3u8_url, flv_url])
    except:
        print('无法获取蓝光地址')

rid = input('请输入快手直播间ID：\n')
room_url = 'https://m.gifshow.com/fw/live/' + str(rid)
headers = {
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'cookie': 'did=web_'}
response = requests.get(url=room_url, headers=headers).text

print('该直播源地址为：')
#print(response)
get_standard_url(response)
get_high_url(response)
get_super_url(response)