# 获取爱奇艺直播的真实流媒体地址。
# iqiyi.js是cmd5x加密函数

import execjs
import json
import requests
import re
import time
import urllib.parse


class IQiYi:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        try:
            response = requests.get('https://m-gamelive.iqiyi.com/w/' + self.rid).text
            # 获取直播间的qipuId
            qipuId = re.findall(r'"qipuId":(\d*?),"roomId', response)[0]
            callback = 'jsonp_' + str(int((time.time() * 1000))) + '_0000'
            params = {
                'lp': qipuId,
                'src': '01010031010000000000',
                'rateVers': 'H5_QIYI',
                'qd_v': 1,
                'callback': callback
            }

            # ba传参iqiyi.js
            ba = '/jp/live?' + urllib.parse.urlencode(params)
            with open('iqiyi.js', 'r') as f:
                content = f.read()
            cmd5x = execjs.compile(content)
            vf = cmd5x.call('cmd5x', ba)

            # 请求
            response = requests.get('https://live.video.iqiyi.com' + ba, params={'vf': vf}).text
            url_json = json.loads(re.findall(r'try{.*?\((.*)\);}catch\(e\){};', response)[0])
            real_url = (url_json.get('data').get('streams'))[0].get('url')
            real_url = real_url.replace('hlslive.video.iqiyi.com', 'm3u8live.video.iqiyi.com')
        except:
            raise Exception('直播间不存在或未开播')
        return real_url


def get_real_url(rid):
    try:
        iqiyi = IQiYi(rid)
        return iqiyi.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入爱奇艺直播房间号：\n')
    print(get_real_url(r))
