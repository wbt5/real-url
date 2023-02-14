# 获取虎牙直播的真实流媒体地址。
import json
import math
import requests
import re
import time
import base64
import hashlib
from urllib.parse import parse_qs, urlencode
from datetime import datetime
import random


def live(info):
    stream_info = dict({'flv': {}, 'hls': {}})
    cdn_type = dict({'AL': '阿里', 'TX': '腾讯', 'HW': '华为', 'HS': '火山'})
    uid = get_anonymous_uid()
    for s in info["roomInfo"]["tLiveInfo"]["tLiveStreamInfo"]["vStreamInfo"]["value"]:
        if s["sFlvUrl"]:
            stream_info["flv"][cdn_type[s["sCdnType"]]] = "{}/{}.{}?{}".format(s["sFlvUrl"], s["sStreamName"],
                                                                               s["sFlvUrlSuffix"],
                                                                               process_anticode(s["sFlvAntiCode"], uid,
                                                                               s["sStreamName"]))
        if s["sHlsUrl"]:
            stream_info["hls"][cdn_type[s["sCdnType"]]] = "{}/{}.{}?{}".format(s["sHlsUrl"], s["sStreamName"],
                                                                               s["sHlsUrlSuffix"],
                                                                               process_anticode(s["sHlsAntiCode"], uid,
                                                                               s["sStreamName"]))
    return stream_info


def process_anticode(anticode, uid, streamname):
    q = dict(parse_qs(anticode))
    q["ver"] = ["1"]
    q["sv"] = ["2110211124"]
    q["seqid"] = [str(int(uid) + int(datetime.now().timestamp() * 1000))]
    q["uid"] = [str(uid)]
    q["uuid"] = [str(get_uuid())]
    ss = hashlib.md5("{}|{}|{}".format(q["seqid"][0], q["ctype"][0], q["t"][0]).encode("UTF-8")).hexdigest()
    q["fm"][0] = base64.b64decode(q["fm"][0]).decode('utf-8').replace("$0", q["uid"][0]).replace("$1",
                                                                                                 streamname).replace(
        "$2", ss).replace("$3", q["wsTime"][0])
    q["wsSecret"][0] = hashlib.md5(q["fm"][0].encode("UTF-8")).hexdigest()
    del q["fm"]
    del q["txyp"]
    return urlencode({x: y[0] for x, y in q.items()})


def get_anonymous_uid():
    url = "https://udblgn.huya.com/web/anonymousLogin"
    resp = requests.post(url, json={
        "appId": 5002,
        "byPass": 3,
        "context": "",
        "version": "2.4",
        "data": {}
    })
    return resp.json()["data"]["uid"]


def get_uuid():
    # Number((Date.now() % 1e10 * 1e3 + (1e3 * Math.random() | 0)) % 4294967295))
    now = datetime.now().timestamp() * 1000
    rand = random.randint(0, 1000) | 0
    return int((now % 10000000000 * 1000 + rand) % 4294967295)


def get_real_url(room_id):
    try:
        room_url = 'https://m.huya.com/' + str(room_id)
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/75.0.3770.100 Mobile Safari/537.36 '
        }
        response = requests.get(url=room_url, headers=header).text
        room_info_str = re.findall(r'\<script\> window.HNF_GLOBAL_INIT = (.*) \</script\>', response)[0]
        room_info = json.loads(room_info_str)
        if room_info["roomInfo"]["eLiveStatus"] == 2:
            print('该直播间源地址为：')
            real_url = json.dumps(live(room_info), indent=2, ensure_ascii=False)
        else:
            real_url = '未开播'

    except Exception as e:
        print(e)
        real_url = '直播间不存在'
    return real_url


rid = input('输入虎牙直播房间号：\n')
real_url = get_real_url(rid)
print(real_url)
