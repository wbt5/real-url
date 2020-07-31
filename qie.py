# 企鹅体育：https://live.qq.com/directory/all
import requests
import re


def qie(rid):
    with requests.Session() as s:
        res = s.get('https://m.live.qq.com/' + str(rid))
    show_status = re.search(r'"show_status":"(\d)"', res.text)
    if show_status:
        if show_status.group(1) == '1':
            hls_url = re.search(r'"hls_url":"(.*)","use_p2p"', res.text).group(1)
            return hls_url
        else:
            raise Exception('未开播')
    else:
        raise Exception('直播间不存在')


if __name__ == '__main__':
    r = input('输入企鹅体育直播间号：\n')
    print(qie(r))
