# 星光直播：https://www.tuho.tv/28545037
import requests
import re


def tuho(rid):
    with requests.Session() as s:
        res = s.get('https://www.tuho.tv/' + str(rid)).text
    flv = re.search(r'videoPlayFlv":"(https[\s\S]+?flv)', res)
    if flv:
        status = re.search(r'isPlaying\s:\s(\w+),', res).group(1)
        if status == 'true':
            real_url = flv.group(1).replace('\\', '')
            return real_url
        else:
            raise Exception('未开播')
    else:
        raise Exception('直播间不存在')


if __name__ == '__main__':
    r = input('输入星光直播房间号：\n')
    print(tuho(r))
