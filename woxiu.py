# 我秀直播：https://www.woxiu.com/

import requests


class WoXiu:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) '
                          'Version/11.0 Mobile/15A372 Safari/604.1'
        }
        url = 'https://m.woxiu.com/index.php?action=M/Live&do=LiveInfo&room_id={}'.format(self.rid)
        with requests.Session() as s:
            res = s.get(url, headers=headers)
        try:
            res = res.json()
        except:
            raise Exception('直播间不存在')
        status = res['online']
        if status:
            live_stream = res['live_stream']
            return live_stream
        else:
            raise Exception('未开播')


def get_real_url(rid):
    try:
        wx = WoXiu(rid)
        return wx.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入我秀直播房间号：\n')
    print(get_real_url(r))
