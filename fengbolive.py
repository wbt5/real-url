# 新浪疯播直播：http://www.fengbolive.com/list?type=hot
# 链接样式：http://www.fengbolive.com/live/88057518
from Crypto.Cipher import AES
from urllib.parse import unquote
import base64
import json
import requests


def fengbo(rid):
    with requests.Session() as s:
        res = s.get('https://external.fengbolive.com/cgi-bin/get_anchor_info_proxy.fcgi?anchorid=' + str(rid)).json()
    if res['ret'] == 1:
        info = res['info']
        info = unquote(info, 'utf-8')

        # 开始AES解密
        def pad(t):
            return t + (16 - len(t) % 16) * b'\x00'

        key = iv = 'abcdefghqwertyui'.encode('utf8')
        cipher = AES.new(key, AES.MODE_CBC, iv)
        info = info.encode('utf8')
        info = pad(info)
        result = cipher.decrypt(base64.decodebytes(info)).rstrip(b'\0')

        result = json.loads(result.decode('utf-8'))
        url = result['url']
        url = url.replace('hdl', 'hls')
        url = url.replace('.flv', '/playlist.m3u8')
        return url
    else:
        raise Exception('房间号错误')


if __name__ == '__main__':
    r = input('输入疯播直播房间号：\n')
    print(fengbo(r))
