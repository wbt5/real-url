# 获取战旗直播（战旗TV）的真实流媒体地址。https://www.zhanqi.tv/lives
# 默认最高画质
import requests


class ZhanQi:

    def __init__(self, rid):
        self.rid = rid

    def get_real_url(self):
        with requests.Session() as s:
            res = s.get('https://m.zhanqi.tv/api/static/v2.1/room/domain/{}.json'.format(self.rid))
            try:
                res = res.json()
                videoid = res['data']['videoId']
                status = res['data']['status']
                if status == '4':
                    url = 'https://dlhdl-cdn.zhanqi.tv/zqlive/{}.flv?get_url=1'.format(videoid)
                    real_url = s.get(url).text
                else:
                    raise Exception('未开播')
            except:
                raise Exception('直播间不存在')
            return real_url


def get_real_url(rid):
    try:
        zq = ZhanQi(rid)
        return zq.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('输入战旗直播房间号：\n')
    print(get_real_url(r))
