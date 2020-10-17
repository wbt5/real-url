# 获取网易云音乐旗下look直播的真实流媒体地址。
# look直播间链接形式：https://look.163.com/live?id=73694082

# 以下核心加密解密算法来自：https://github.com/Qinjiaxin/MusicBox/blob/b8f716d43d/MusicPlayer/apis/netEaseEncode.py
# 分析过程可参看 https://github.com/Qinjiaxin/MusicBox/blob/b8f716d43d/doc/analysis/analyze_captured_data.md

# 加密参数相关。
# 具体http://s3.music.126.net/sep/s/2/core.js?5d6f8e4d01b4103ec9f246a2ef70e6d1在这个js中可以查看。
# 好吧，其实不用分析这个js，在这个git中可以找到https://github.com/xiyouMc/ncmbot，不过他是for python2的。
# 针对pyton3做了修改。

import base64
import binascii
import json
import random

import requests
from Crypto.Cipher import AES

modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
nonce = b'0CoJUm6Qyw8W8jud'
pubKey = '010001'


def aes_encrypt(text, secKey):
    pad = 16 - len(text) % 16

    # aes加密需要byte类型。
    # 因为调用两次，下面还要进行补充位数。
    # 直接用try与if差不多。

    try:
        text = text.decode()
    except:
        pass

    text = text + pad * chr(pad)
    try:
        text = text.encode()
    except:
        pass

    encryptor = AES.new(secKey, 2, bytes('0102030405060708', 'utf-8'))
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext


def create_secret_key(size):
    # 2中 os.urandom返回是个字符串。3中变成bytes。
    # 不过加密的目的是需要一个字符串。
    # 因为密钥之后会被加密到rsa中一起发送出去。
    # 所以即使是个固定的密钥也是可以的。

    # return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]
    return bytes(''.join(random.sample('1234567890qwertyuipasdfghjklzxcvbnm', size)), 'utf-8')


def rsa_encrypt(text, pub_key, modulus):
    text = text[::-1]
    # 3中将字符串转成hex的函数变成了binascii.hexlify, 2中可以直接 str.encode('hex')
    rs = int(binascii.hexlify(text), 16) ** int(pub_key, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)


def encrypted_request(text):
    # 这边是加密过程。
    text = json.dumps(text)
    sec_key = create_secret_key(16)
    enc_text = aes_encrypt(aes_encrypt(text, nonce), sec_key)
    enc_sec_key = rsa_encrypt(sec_key, pubKey, modulus)
    # 在那个js中也可以找到。
    # params加密后是个byte，解下码。
    return {'params': enc_text.decode(), 'encSecKey': enc_sec_key}


class Look:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        try:
            request_data = encrypted_request({"liveRoomNo": self.rid})
            response = requests.post(url='https://api.look.163.com/weapi/livestream/room/get/v3',
                                     data=request_data)
            real_url = response.json()['data']['roomInfo']['liveUrl']

        except:
            raise Exception('直播间不存在或未开播')
        return real_url


def get_real_url(rid):
    try:
        look = Look(rid)
        return look.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入Look直播房间号：\n')
    print(get_real_url(r))
