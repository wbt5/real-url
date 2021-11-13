# 红人直播：https://www.hongle.tv/
# 该平台需登陆，下面代码中已集成一个账号的登陆方式；
# 如登陆信息过期，可用自己的账号登陆后，查找浏览器Local Storage中的hrtk字段，替换代码中的accesstoken

from urllib.parse import urlencode
from urllib.parse import unquote
import requests
import time
import hashlib
import json


class HongLe:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        # 模拟登陆
        with requests.Session() as s:
            pass

        tt = int(time.time() * 1000)
        url = f'https://service.hongle.tv/v2/userw/login?_st1={tt}'
        data = {
            '_st1': tt,
            'geetest_challenge': '7f4f6fd6257799c0bcac1f38c21c042dl0',
            'geetest_seccode': 'd1163915f4cfd6c998014c4ca8899c9d|jordan',
            'geetest_validate': 'd1163915f4cfd6c998014c4ca8899c9d',
            'name': '16530801176',
            'password': 'QTXz9/Sp40BbMHwVtcb7AQ==',
        }

        data1 = urlencode(data) + 'yuj1ah5o'
        _ajaxdata1 = hashlib.md5(data1.encode('utf-8')).hexdigest()
        data['_ajaxData1'] = _ajaxdata1
        del data['_st1']
        data = json.dumps(data, separators=(',', ':'))
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        res = s.post(url, data=data, headers=headers).json()
        if res['status']['statuscode'] == '0':
            sessionid = res['data']['sessionid']
        else:
            raise Exception('登陆信息过期')

        url = 'https://service.hongle.tv/v2/roomw/media'
        accesstoken = sessionid
        params = {
            '_st1': tt,
            'accessToken': accesstoken,
            'of': 1,
            'showid': self.rid,
            'tku': 43112608,
        }
        data = urlencode(params) + 'yuj1ah5o'
        _ajaxData1 = hashlib.md5(data.encode('utf-8')).hexdigest()
        params['_ajaxData1'] = _ajaxData1
        params['accessToken'] = unquote(accesstoken)

        res = s.get(url, params=params)
        if res.status_code == 200:
            res = res.json()
            statuscode = res['status']['statuscode']
            if statuscode == '0':
                if res['data']['live_status'] == '1':
                    real_url = res['data']['media_url_web']
                    real_url = real_url.replace('http', 'https')
                    real_url = real_url.replace('__', '&')
                    return real_url
                else:
                    raise Exception('未开播')
            else:
                raise Exception('房间不存在')
        else:
            raise Exception('参数错误')


def get_real_url(rid):
    try:
        hl = HongLe(rid)
        return hl.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('输入红人直播房间号：\n')
    print(get_real_url(r))
