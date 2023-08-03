# 获取斗鱼直播间的真实流媒体地址，默认最高画质
import hashlib
import re
import time
import execjs
import requests
import json


class DouYu:

    def __init__(self, rid):
        """
        房间号通常为1~8位纯数字，浏览器地址栏中看到的房间号不一定是真实rid.
        Args:
            rid:
        """
        self.did = '10000000000000000000000000001501'
        self.t10 = str(int(time.time()))
        self.t13 = str(int((time.time() * 1000)))

        self.s = requests.Session()
        self.res = self.s.get('https://m.douyu.com/' + str(rid)).text
        result = re.search(r'rid":(\d{1,8}),"vipId', self.res)

        if result:
            self.rid = result.group(1)
        else:
            raise Exception('房间号错误')

    @staticmethod
    def md5(data):
        return hashlib.md5(data.encode('utf-8')).hexdigest()

    def get_pre(self):
        url = 'https://playweb.douyucdn.cn/lapi/live/hlsH5Preview/' + self.rid
        data = {
            'rid': self.rid,
            'did': self.did
        }
        auth = DouYu.md5(self.rid + self.t13)
        headers = {
            'rid': self.rid,
            'time': self.t13,
            'auth': auth
        }
        res = self.s.post(url, headers=headers, data=data).json()
        error = res['error']
        return error

    def get_did(self):
        did = '10000000000000000000000000001501'
        url = "https://passport.douyu.com/lapi/did/api/get?client_id=25&_={}&callback=axiosJsonpCallback1".format(self.t13)
        headers = {
            'referer': 'https://m.douyu.com/'
        }
        try:
            res = self.s.get(url=url,headers=headers).text
            result = json.loads(re.search(r"axiosJsonpCallback1\((.*)\)", res).group(1))
            if result["error"] == 0:
                if "did" in result["data"]:
                    did = result["data"]["did"]
        except Exception as e:
            print(e)
        return did

    def get_js(self):
        result = re.search(r'(function ub98484234.*)\s(var.*)', self.res).group()
        func_ub9 = re.sub(r'eval.*;}', 'strc;}', result)
        js = execjs.compile(func_ub9)
        res = js.call('ub98484234')

        v = re.search(r'v=(\d+)', res).group(1)
        rb = DouYu.md5(self.rid + self.did + self.t10 + v)

        func_sign = re.sub(r'return rt;}\);?', 'return rt;}', res)
        func_sign = func_sign.replace('(function (', 'function sign(')
        func_sign = func_sign.replace('CryptoJS.MD5(cb).toString()', '"' + rb + '"')

        js = execjs.compile(func_sign)
        params = js.call('sign', self.rid, self.did, self.t10)
        params += '&ver=22107261&rid={}&rate=-1'.format(self.rid)

        url = 'https://m.douyu.com/api/room/ratestream'
        res = self.s.post(url, params=params).json()
        return res

    def get_real_url(self):
        real_url = {}
        error = self.get_pre()
        if error == 102:
            raise Exception('房间不存在')
        elif error == 104:
            raise Exception('房间未开播')
        else:
            try:
                data = self.get_js()
                real_url["m3u8"] = data["data"]["url"]
            except:
                pass
        return json.dumps(real_url, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    r = input('输入斗鱼直播间号：\n')
    s = DouYu(r)
    s.did = s.get_did()
    print(s.get_real_url())

