# 热猫直播：https://zhibo.yuanbobo.com/
import requests
import re


def yuanbobo(rid):
    with requests.Session() as s:
        res = s.get('https://zhibo.yuanbobo.com/' + str(rid)).text
    stream_id = re.search(r"stream_id:\s+'(\d+)'", res)
    if stream_id:
        status = re.search(r"status:\s+'(\d)'", res).group(1)
        if status == '1':
            real_url = 'http://ks-hlslive.yuanbobo.com/live/{}/index.m3u8'.format(stream_id.group(1))
            return real_url
        else:
            raise Exception('未开播')
    else:
        raise Exception('直播间不存在')


if __name__ == '__main__':
    r = input('输入热猫直播房间号：\n')
    print(yuanbobo(r))
