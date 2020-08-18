# 获取快手直播的真实流媒体地址，默认输出最高画质

import json
import re

import requests


def kuaishou(rid):
    headers = {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 '
                      '(KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'cookie': 'did=web_'}
    with requests.Session() as s:
        res = s.get('https://m.gifshow.com/fw/live/{}'.format(rid), headers=headers)
        livestream = re.search(r'liveStream":(.*),"obfuseData', res.text)
        if livestream:
            livestream = json.loads(livestream.group(1))
            *_, hlsplayurls = livestream['multiResolutionHlsPlayUrls']
            urls, = hlsplayurls['urls']
            url = urls['url']
            return url
        else:
            raise Exception('直播间不存在或未开播')


if __name__ == '__main__':
    r = input('输入快手直播房间号：\n')  # 例：jjworld126
    print(kuaishou(r))
