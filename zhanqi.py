# 获取战旗直播（战旗TV）的真实流媒体地址。https://www.zhanqi.tv/lives
# 默认最高画质
import requests


def zhanqi(rid):
    with requests.Session() as s:
        res = s.get('https://m.zhanqi.tv/api/static/v2.1/room/domain/{}.json'.format(rid))
        try:
            res = res.json()
            videoid = res['data']['videoId']
            status = res['data']['status']
            if status == '4':
                url = 'https://dlhdl-cdn.zhanqi.tv/zqlive/{}.flv?get_url=1'.format(videoid)
                real_url = s.get(url).text
            else:
                real_url = '未开播'
        except:
            real_url = '直播间不存在'
        return real_url


if __name__ == '__main__':
    r = input('输入战旗直播房间号：\n')
    print(zhanqi(r))
