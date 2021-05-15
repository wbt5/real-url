# 获取爱奇艺直播的真实流媒体地址。
# iqiyi.js是cmd5x加密函数

import json
import re
import time
import urllib.parse

import execjs
import requests


class IQiYi:
    """获取爱奇艺 m3u8 格式直播源

    输入房间号，通常是数字，比如链接 https://gamelive.iqiyi.com/w/74429 中的 74429。
    注意：
        爱奇艺有部分直播是来自pps的，要打开房间看链接是否有跳转，有则用pps.py
        爱奇艺直播依赖js环境，建议安装node.js。

    Attributes:
        rid:    房间号
    """

    def __init__(self, rid):
        self.rid = rid
        self.s = requests.Session()

    def get_real_url(self):
        """
        里面iqiyi.js是个加盐的md5，execjs执行后获取cmd5x的返回值

        Returns:
            m3u8格式播放地址

        Raises:
            incorrect rid: 请确实是爱奇艺直播房间号：爱奇艺有部分直播是来自pps的，要打开房间看链接是否有跳转，有则用pps.py
            Could not find an available JavaScript runtime: 是否安装了js环境

        """

        res = self.s.get('https://m-gamelive.iqiyi.com/w/' + self.rid).text
        # 获取直播间的qipuId
        try:
            qipuid, = re.findall(r'"qipuId":(\d*?),"roomId', res)
        except ValueError:
            raise Exception('Incorrect rid.')

        callback = 'jsonp_' + str(int((time.time() * 1000))) + '_0000'
        params = {
            'lp': qipuid,
            'src': '01010031010000000000',
            'rateVers': 'H5_QIYI',
            'qd_v': 1,
            'callback': callback
        }
        # ba传参iqiyi.js,返回vf
        ba = '/jp/live?' + urllib.parse.urlencode(params)
        with open('iqiyi.js', 'r') as f:
            content = f.read()
        try:
            cmd5x = execjs.compile(content)
            vf = cmd5x.call('cmd5x', ba)
        except RuntimeError:
            raise Exception('Could not find an available JavaScript runtime.')
        # 请求
        response = self.s.get('https://live.video.iqiyi.com' + ba, params={'vf': vf}).text
        url_json = json.loads(re.findall(r'try{.*?\((.*)\);}catch\(e\){};', response)[0])
        url = (url_json.get('data').get('streams'))[0].get('url')
        url = url.replace('hlslive.video.iqiyi.com', 'm3u8live.video.iqiyi.com')

        return url


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
