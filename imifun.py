# 艾米直播：https://www.imifun.com/
import requests
import re


def imifun(rid):
    with requests.Session() as s:
        res = s.get('https://www.imifun.com/' + str(rid)).text
    roomid = re.search(r"roomId:\s'([\w-]+)'", res)
    if roomid:
        status = re.search(r"isLive:(\d),", res).group(1)
        if status == '1':
            real_url = 'https://wsmd.happyia.com/ivp/{}.flv'.format(roomid.group(1))
            return real_url
        else:
            raise Exception('未开播')
    else:
        raise Exception('直播间不存在')


if __name__ == '__main__':
    r = input('输入艾米直播房间号：\n')
    print(imifun(r))
