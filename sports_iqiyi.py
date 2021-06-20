# -*- coding: utf-8 -*-
# @Time: 2021/6/19 20:39
# @Project: my-spiders
# @Author: wbt5
# @Blog: https://wbt5.com


import binascii
import hashlib
import json
import re
import time
from urllib.parse import urlencode

import execjs
import requests


class sIQiYi:

    def __init__(self, rid):
        url = rid
        self.rid = url.split('/')[-1]
        self.s = requests.Session()

    def decodeurl(self):
        """
        传入url地址，截取url中的直播间id
        字符串lgqipu倒序后转为十进制数，作为qpid解码的传参
        Returns:
            qpid
        """
        o = 'lgqipu'
        o = int(binascii.hexlify(o[::-1].encode()), 16)

        s = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        a = 0
        rr = enumerate(self.rid)
        for i, _ in rr:
            a += s.index(_) * pow(36, len(self.rid) - (i + 1))

        a = f'{a:b}'
        n = f'{o:b}'
        x = len(a)
        y = len(n)
        if x > y:
            i = a[:x - y]
            a = a[x - y:]
        else:
            i = n[:y - x]
            n = n[y - x:]

        for r in range(0, len(a)):
            if a[r] == n[r]:
                i += '0'
            else:
                i += '1'
        qpid = int(i, 2)
        return qpid

    def get_real_url(self):
        """
        里面iqiyi.js是个加盐的md5，execjs执行后获取cmd5x的返回值
        Returns:
            m3u8格式播放地址
        Raises:
            Could not find an available JavaScript runtime: 是否安装了js环境
        """
        qpid = self.decodeurl()
        uid = 'ba4fe551bd889d73f3d321d2fadc6130'
        ve = hashlib.md5(f'{qpid}function getTime() {{ [native code] }}{uid}'.encode('utf-8')).hexdigest()
        v = {
            'lp': qpid,
            'src': '01014351010000000000',
            'ptid': '02037251010000000000',
            'uid': '',
            'rateVers': 'H5_QIYI',
            'k_uid': uid,
            'qdx': 'n',
            'qdv': 3,
            'dfp': '',
            've': ve,
            'v': 1,
            'k_err_retries': 0,
            'tm': int(time.time()),
            'k_ft4': 17179869185,
            'k_ft1': 141287244169216,
            'k_ft5': 1,
            'qd_v': 1,
            'qdy': 'a',
            'qds': 0,
            # 'callback': 'Q3d080ff19d8f233acb05683bf38e3a15',
            # 'vf': 'f0b986f100ae81fff8e8f8f96053e815',
        }
        k = '/jp/live?' + urlencode(v)
        cb = hashlib.md5(k.encode('utf-8')).hexdigest()
        k = f'{k}&callback=Q{cb}'

        # 生成vf
        with open('iqiyi.js', 'r') as f:
            content = f.read()
        try:
            cmd5x = execjs.compile(content)
            vf = cmd5x.call('cmd5x', k)
        except RuntimeError:
            raise Exception('Could not find an available JavaScript runtime.')

        # 请求url
        url = f'https://live.video.iqiyi.com{k}&vf={vf}'
        res = self.s.get(url).text

        try:
            res, = re.findall(r'try{[\s\S]{33}\((.*)\);}catch\(e\){};', res)
            url = json.loads(res)['data']['streams'][-1]['url']
        except ValueError:
            raise Exception('Incorrect rid.')
        return url


def get_real_url(rid):
    try:
        siqiyi = sIQiYi(rid)
        return siqiyi.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入爱奇艺体育直播间完整地址地址，注意只能获取免费直播：\n')
    # https://sports.iqiyi.com/resource/pcw/live/gwbgbfbgc3
    print(get_real_url(r))
