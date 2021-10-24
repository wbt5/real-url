# 获取哔哩哔哩直播的真实流媒体地址，默认获取直播间提供的最高画质
# qn=150高清
# qn=250超清
# qn=400蓝光
# qn=10000原画
import requests


class BiliBili:

    def __init__(self, rid):
        rid = rid
        self.header = {
            'User-Agent': 'Mozilla/5.0 (iPod; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.163 Mobile/15E148 Safari/604.1',
        }
        # 先获取直播状态和真实房间号
        r_url = 'https://api.live.bilibili.com/room/v1/Room/room_init'
        param = {
            'id': rid
        }
        with requests.Session() as s:
            res = s.get(r_url, headers=self.header, params=param).json()
        if res['msg'] == '直播间不存在':
            print(f'bilibili {rid} {res["msg"]}')
        live_status = res['data']['live_status']
        if live_status != 1:
            print(f'bilibili {rid} 未开播')
        self.real_room_id = res['data']['room_id']

    def get_stream_address(self, current_qn: int = 10000) -> list:
        url = 'https://api.live.bilibili.com/xlive/web-room/v2/index/getRoomPlayInfo'
        param = {
            'device': 'pc',
            'platform': 'h5',
            'scale': 0,
            'build': '10000',
            'protocol': '0,1',
            'format': '0,1,2',
            'codec': '0,1',
            'room_id': self.real_room_id,
            'qn': current_qn
        }
        with requests.Session() as session:
            res = session.get(url, headers=self.header, params=param)
            res = res.json()
            stream_info = res['data']['playurl_info']['playurl']['stream']
            qn_max = 0
            for data in stream_info:
                accept_qn = data['format'][0]['codec'][0]['accept_qn']
                for qn in accept_qn:
                    qn_max = qn if qn > qn_max else qn_max
            if qn_max != current_qn:
                param['qn'] = qn_max
                res = session.get(url, headers=self.header, params=param)
                res = res.json()
                stream_info = res['data']['playurl_info']['playurl']['stream']
            stream_url_list = []
            for data in stream_info:
                format_name = data['format'][0]['format_name']
                if format_name == 'flv':
                    base_url = data['format'][0]['codec'][0]['base_url']
                    url_info = data['format'][0]['codec'][0]['url_info']
                    for info in url_info:
                        host = info['host']
                        extra = info['extra']
                        # print(host + base_url + extra)
                        stream_url_list.append(host + base_url + extra)
                    break
            return stream_url_list


if __name__ == '__main__':
    rid = input('请输入bilibili直播房间号：\n')
    bilibili = BiliBili(rid)
    print(bilibili.get_stream_address())
