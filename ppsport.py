# -*- coding: utf-8 -*-
# @Time: 2021/5/4 15:11
# @Project: real-url
# @Author: wbt5
# @Blog: https://wbt5.com

import base64
import binascii
from urllib.parse import parse_qsl, urlsplit, urlencode

import requests
from Crypto.Cipher import AES, DES3
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


def des_encrypt(text, key, iv):
    """
    DES加密
    """
    key = binascii.a2b_hex(key)
    iv = binascii.a2b_hex(iv)
    pad = 8 - len(text) % 8
    text = text + pad * chr(pad)
    text = text.encode()
    cipher = DES3.new(key, DES3.MODE_CBC, iv)
    encrypt_bytes = cipher.encrypt(text)
    return base64.b64encode(encrypt_bytes).decode('utf-8')


def rsa_encrypt(text):
    """
    RSA加密
    :param text:
    :return:
    """
    pub_key = '-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqe6XLQF2JmXWgfh09t8TTZsOb6bnj' \
              '+duiWw4G7pd5Uo1/DN7Xij3Tys9E7XBX0gdXKYI9j+6Fr45bM28fzl4AxUxnhzmbExRt1NJarDGMKo49ViRg1VbL+Wh9kRi' \
              '+rAxBisdRiP2JEAL+Awqu80chZxxdyoI1k3fSLoZsv/PGkwolE71qsEM4BO1J9RWNp0wlNGqgR' \
              '+bTwLKkoe7oiZaKaMsSBWNIBDkwgGKFJZzXMXMnqGsDmfbdi32j6hW9DdrxjCx' \
              '/i9Nzahd1TWVnw9O1AHL5PD5kM3HzqkAewBu38sZxw8DSGYqG0fgVAQtiLHhlD/19F4NKxqL8IVCinMBHQIDAQAB\n-----END ' \
              'PUBLIC KEY----- '
    pub_key = RSA.importKey(pub_key)
    cipher = PKCS1_v1_5.new(pub_key)
    rsa_text = base64.b64encode(cipher.encrypt(bytes(text.encode("utf8"))))
    return rsa_text.decode('utf-8')


def encrypt(params):
    """
    encrypt_params是DES3加密,cipher是RSA加密
    :param params:
    :return:
    """
    key = 'DB30EB9226014FEC2A04C6A7BE47F22853B6621BD6989D83'
    iv = '6795646FD1F8CC95'
    encrypt_params = des_encrypt(urlencode(params, safe=','), key, iv)
    cipher = rsa_encrypt(f'{key},{iv}')
    en_params = {
        'cipher': cipher,
        'encryptParams': encrypt_params,
        'vvId': '295b5e4a-4a77-442a-8594-36c47c87d6c5',
        # 'format': 'jsonp'
    }
    return en_params


def aes_decrypt(text, key):
    """
    aes解密，ECB模式，key先hash
    :param text:密文
    :param key:key
    :return:
    """
    h = SHA256.new()
    h.update(key.encode())
    key = h.hexdigest()
    key = binascii.a2b_hex(key)
    cipher = AES.new(key, AES.MODE_ECB)
    text = binascii.a2b_hex(text)
    decrypt_key = cipher.decrypt(text)
    return binascii.b2a_hex(decrypt_key).decode()


class PPSport:
    """
    链接样式：http://sports.pptv.com/sportslive/pg_h5live?sectionid=184978

     - liveFlag=1 正在直播
     - liveFlag=2 没有直播，有录像集锦
     - liveFlag 为空，没有录像

    非VIP最高获取1280P
    """

    def __init__(self, rid):
        # 拆分sectionid
        var = dict(parse_qsl(urlsplit(rid).query))
        sectionid = var.get('sectionid')
        if sectionid:
            self.sectionid = sectionid
        else:
            raise Exception('Invalid link!')
        # 获取cid
        with requests.Session() as self.s:
            res = self.s.get(f'http://sportlive.suning.com/slsp-web/cms/competitionschedule/v1/detail/section.do'
                             f'?sectionid={sectionid}').json()

            self.liveflag = res['data'].get('liveFlag')

            if self.liveflag == '1':
                # 正在直播
                self.cid = res['data']['sectionInfo']['lives'][0]['cid']
            elif self.liveflag == '2':
                # 录像
                try:
                    self.cid = res['data']['sectionInfo']['lives'][0]['afterCid']
                except KeyError:
                    # 没有录像
                    raise Exception('No streaming!')
            else:
                raise Exception('liveflag error!')

    def get_real_url(self):
        """
        PPSport原网页中会把下面的params加密后再发送请求，用上面的encrypt，这里请求参数不加密也可以
        :return:url
        """
        params = {
            'type': 'mhpptv',
            'appId': 'pptv.web.h5',
            'appPlt': 'web',
            'appVer': '1.0.4',
            'channel': 'sn.cultural',
            'sdkVer': '1.5.0',
            'cid': self.cid,
            'allowFt': '0,1,2,3',
            'rf': 0,
            'ppi': '302c3530',
            'o': 0,
            'ahl_ver': 1,
            'ahl_random': '374b7d5d453b2c4d2e2e327452434168',
            'ahl_signa': '552aed5c0f2d2e561cd55991925ae817add78ceb86ede3ecac08dd4df6a31f78',
            'version': 1,
            'streamFormat': 1,
            'videoFormat': 'm3u8',
            'vvId': '295b5e4a-4a77-442a-8594-36c47c87d6c5',
        }
        # params = encrypt(params)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/90.0.4430.93 Safari/537.36 ',
        }
        res = self.s.get('http://oneplay.api.pptv.com/ups-service/play', headers=headers, params=params)
        res = res.json()

        if res.get('code', 1) == 0:
            if self.liveflag == '1':
                # 正在直播
                vod2 = res['data']['program']['media']['resource']['stream']['live2']
            else:
                # 录像集锦
                vod2 = res['data']['program']['media']['resource']['vod2']

            delay = vod2.get('delay')
            interval = vod2.get('interval')

            item = vod2['item'][-1]
            dt = item['dt']
            rid = item['rid'].split('.')[0]

            if self.liveflag == '1':
                h = dt['sh']['content'] + dt['st'] + dt['bh']['content'] + dt['iv'] + 'V8oo0Or1f047NaiMTxK123LMFuINTNeI'
            else:
                h = dt['sh'] + dt['st'] + dt['id'] + dt['bh'] + dt['iv'] + 'V8oo0Or1f047NaiMTxK123LMFuINTNeI'

            key = dt['key']['content']
            key, n = key.split('-', 1)
            # 解密获取k
            k = aes_decrypt(key, h) + '-' + n
            k = {
                'h5vod.ver': '2.1.5',
                'k': k,
                'vvid': '295b5e4a-4a77-442a-8594-36c47c87d6c5',
                'type': 'mhpptv',
                'o': 0,
                'sv': '4.1.18',
            }

            url = f"http://{dt['bh']['content']}/live/{interval}/{delay}/{rid}.m3u8?playback=0&{urlencode(k)}" \
                if self.liveflag == '1' else f"http://{dt['bh']}/{rid}.m3u8?fpp.ver=1.0.0&{urlencode(k)}"
            return url
        else:
            raise Exception('Invalid parameters')


def get_real_url(rid):
    try:
        pps = PPSport(rid)
        return pps.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入PP体育直播间地址：\n')
    print(get_real_url(r))
