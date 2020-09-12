# 获取56千帆直播的真实流媒体地址。
# 千帆直播直播间链接形式：https://qf.56.com/520686

import requests
import re


class QF:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        try:
            response = requests.post(url='https://qf.56.com/' + self.rid).text
            real_url = re.findall(r"flvUrl:'(.*)\?wsSecret", response)
            real_url = real_url[0]
        except:
            raise Exception('直播间不存在或未开播')
        return real_url


def get_real_url(rid):
    try:
        qf = QF(rid)
        return qf.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入千帆直播房间号：\n')
    print(get_real_url(r))
