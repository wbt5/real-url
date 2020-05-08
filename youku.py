# 获取@优酷轮播台@的真实流媒体地址。
# 优酷轮播台是优酷直播live.youku.com下的一个子栏目，轮播一些经典电影电视剧，个人感觉要比其他直播平台影视区的画质要好，而且没有平台水印和主播自己贴的乱七八糟的字幕遮挡。
# liveId 是如下形式直播间链接“https://vku.youku.com/live/ilproom?spm=a2hcb.20025885.m_16249_c_59932.d_11&id=8019610&scm=20140670.rcmd.16249.live_8019610”中的8019610字段。


import requests
import time
import hashlib
import json


def get_real_url(liveId):
    try:
        tt = str(int(time.time()*1000))
        data = json.dumps({"liveId":liveId,"app":"Pc"}, separators=(',', ':'))
        url = 'https://acs.youku.com/h5/mtop.youku.live.com.livefullinfo/1.0/?appKey=24679788'
        s = requests.Session()
        cookies = s.get(url).cookies
        token = requests.utils.dict_from_cookiejar(cookies).get('_m_h5_tk')[0:32]
        sign = hashlib.md5((token + '&' + tt + '&' + '24679788' + '&' + data).encode('utf-8')).hexdigest()
        params = {
            't': tt,
            'sign': sign,
            'data': data
        }
        response = s.get(url, params=params).json()
        name = response.get('data').get('data').get('name')
        streamName = response.get('data').get('data').get('stream')[0].get('streamName')
        real_url = 'http://lvo-live.youku.com/vod2live/{}_mp4hd2v3.m3u8?&expire=21600&psid=1&ups_ts={}&vkey='.format(streamName, int(time.time()))
    except:
        name = real_url = '请求错误'
    return name, real_url


liveId = input('请输入优酷轮播台liveId：\n')
real_url = get_real_url(liveId)
print('该直播间地址为：')
print(real_url[0])
print(real_url[1])
