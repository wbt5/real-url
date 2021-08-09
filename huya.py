# 获取虎牙直播的真实流媒体地址。
# 虎牙"一起看"频道的直播间可能会卡顿，尝试将返回地址 tx.hls.huya.com 中的 tx 改为 bd、migu-bd。

import requests
import re
import base64
import urllib.parse
import hashlib
import time
import json


class HuYa:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        try:
            room_url = 'https://m.huya.com/' + str(self.rid)
            header = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 '
                              '(KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36 '
            }
            response = requests.get(url=room_url, headers=header).text
            info = json.loads(re.findall(r"<script> window.HNF_GLOBAL_INIT = (.*)</script>", response)[0])
            if info == {'exceptionType': 0}:
                raise Exception('房间不存在')
            roomInfo = info["roomInfo"]
            real_url = {}

            # not live
            if roomInfo["eLiveStatus"] == 1:
                raise Exception('未开播')

            # live
            elif roomInfo["eLiveStatus"] == 2:
                streamInfos = roomInfo["tLiveInfo"]["tLiveStreamInfo"]["vStreamInfo"]["value"]
                for streamInfo in streamInfos:
                    real_url[streamInfo["sCdnType"].lower() + "_flv"] = streamInfo["sFlvUrl"] + "/" + streamInfo["sStreamName"] + "." + \
                                                                  streamInfo["sFlvUrlSuffix"] + "?" + streamInfo["sFlvAntiCode"]
                    real_url[streamInfo["sCdnType"].lower() + "_hls"] = streamInfo["sHlsUrl"] + "/" + streamInfo["sStreamName"] + "." + \
                                                                  streamInfo["sHlsUrlSuffix"] + "?" + streamInfo["sHlsAntiCode"]

            # replay
            elif roomInfo["eLiveStatus"] == 3:
                real_url["replay"] = roomInfo["tReplayInfo"]["tReplayVideoInfo"]["sUrl"]
            else:
                raise Exception('未知错误')
        except Exception as e:
            raise Exception(e)
        return real_url


def get_real_url(rid):
    try:
        hy = HuYa(rid)
        return hy.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    rid = input('输入虎牙直播房间号：\n')
    print(get_real_url(rid))