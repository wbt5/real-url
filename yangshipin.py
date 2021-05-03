# -*- coding: utf-8 -*-
# @Time: 2021/5/3 12:28
# @Project: real-url
# @Author: wbt5
# @Blog: https://wbt5.com

# CCTV-1: https://m.yangshipin.cn/video?type=1&vid=2000210103&pid=600001859
# 需要替换 headers 中登陆的 cookie
# 目前网页版链接有效时间很短，且每个IP每天的请求数量有限制
# APP版本的链接放时间更长，但需要反编译获取ckey生成方式，以后再更新。

import binascii
import ctypes
import time
import uuid
from urllib.parse import parse_qs

import requests
from Crypto.Cipher import AES


def aes_encrypt(text):
    """
    AES加密
    """
    key = binascii.a2b_hex('4E2918885FD98109869D14E0231A0BF4')
    iv = binascii.a2b_hex('16B17E519DDD0CE5B79D7A63A4DD801C')
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    text = text.encode()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypt_bytes = cipher.encrypt(text)
    return binascii.b2a_hex(encrypt_bytes).decode()


class YangShiPin:

    def __init__(self, rid):
        var = parse_qs(rid)
        vid, = var['vid']
        pid, = var['pid']

        platform = 4330701
        guid = 'ko7djb70_vbjvrg5gcm'
        txvlive_version = '3.0.37'
        tt = int(time.time())
        jc = 'mg3c3b04ba'
        wu = f'|{vid}|{tt}|{jc}|{txvlive_version}|{guid}|{platform}|https://m.yangshipin.cn/|mozilla/5.0 (iphone; ' \
             f'cpu||Mozilla|Netscape|Win32| '

        u = 0
        for i in wu:
            _char = ord(i)
            u = (u << 5) - u + _char
            u &= u & 0xffffffff
        bu = ctypes.c_int32(u).value

        xu = f'|{bu}{wu}'
        # ckey是个aes加密，CBC模式，pkcs7填充
        ckey = ('--01' + aes_encrypt(xu)).upper()

        self.params = {
            'cmd': 2,
            'cnlid': vid,
            'pla': 0,
            'stream': 2,
            'system': 1,
            'appVer': '3.0.37',
            'encryptVer': '8.1',
            'qq': 0,
            'device': 'PC',
            'guid': 'ko7djb70_vbjvrg5gcm',
            'defn': 'auto',
            'host': 'yangshipin.cn',
            'livepid': pid,
            'logintype': 1,
            'vip_status': 1,
            'livequeue': 1,
            'fntick': tt,
            'tm': tt,
            'sdtfrom': 113,
            'platform': platform,
            'cKey': ckey,
            'queueStatus': 0,
            'uhd_flag': 4,
            'flowid': uuid.uuid4().hex,
            'sphttps': 1,
            # 'callback': 'txvlive_videoinfoget_9046016361',
        }

    def get_real_url(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                          'like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'referer': 'https://m.yangshipin.cn/',
            'cookie': ''
        }
        res = requests.get('https://liveinfo.yangshipin.cn/', headers=headers, params=self.params).json()
        url = res.get('playurl', 0)
        if url:
            return url
        else:
            return res


def get_real_url(rid):
    try:
        ysp = YangShiPin(rid)
        return ysp.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('显示“无登录信息”，则需要填充cookie。请输入央视频地址：\n')
    print(get_real_url(r))
