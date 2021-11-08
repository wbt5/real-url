# 获取网易CC的真实流媒体地址。
# 默认为最高画质

import requests


class CC:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        room_url = f'https://api.cc.163.com/v1/activitylives/anchor/lives?anchor_ccid={self.rid}'
        response = requests.get(url=room_url).json()
        data = response.get('data', 0)
        if data:
            channel_id = data.get(f'{self.rid}').get('channel_id', 0)
            if channel_id:
                response = requests.get(f'https://cc.163.com/live/channel/?channelids={channel_id}').json()
                real_url = response.get('data')[0].get('sharefile')
            else:
                raise Exception('直播间不存在')
        else:
            raise Exception('输入错误')
        return real_url


def get_real_url(rid):
    try:
        cc = CC(rid)
        return cc.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入网易CC直播房间号：\n')
    print(get_real_url(r))
