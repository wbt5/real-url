# 获取哔哩哔哩直播的真实流媒体地址，默认获取直播间提供的最高画质
# qn=150高清
# qn=250超清
# qn=400蓝光
# qn=10000原画
import requests


def bilibili(rid):
    # 先获取直播状态和真实房间号
    r_url = 'https://api.live.bilibili.com/room/v1/Room/room_init?id={}'.format(rid)
    with requests.Session() as s:
        res = s.get(r_url).json()
    code = res['code']
    if code == 0:
        live_status = res['data']['live_status']
        if live_status == 1:
            room_id = res['data']['room_id']

            def u(pf):
                f_url = 'https://api.live.bilibili.com/xlive/web-room/v1/playUrl/playUrl'
                params = {
                    'cid': room_id,
                    'qn': 10000,
                    'platform': pf,
                    'https_url_req': 1,
                    'ptype': 16
                }
                resp = s.get(f_url, params=params).json()
                try:
                    durl = resp['data']['durl']
                    real_url = durl[-1]['url']
                    return real_url
                except KeyError or IndexError:
                    raise Exception('获取失败')

            return {
                'flv_url': u('web'),
                'hls_url': u('h5')
            }

        else:
            raise Exception('未开播')
    else:
        raise Exception('房间不存在')


if __name__ == '__main__':
    r = input('输入bilibili直播间号：\n')
    print(bilibili(r))
