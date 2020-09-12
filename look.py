# 获取网易云音乐旗下look直播的真实流媒体地址。
# look直播间链接形式：https://look.163.com/live?id=73694082

import requests
import re


class Look:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        try:
            response = requests.post(url='https://look.163.com/live?id=' + self.rid).text
            real_url = re.findall(r'"liveUrl":([\s\S]*),"liveType"', response)[0]
        except:
            raise Exception('直播间不存在或未开播')
        return real_url


def get_real_url(rid):
    try:
        look = Look(rid)
        return look.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入Look直播房间号：\n')
    print(get_real_url(r))

