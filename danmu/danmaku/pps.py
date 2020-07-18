import hashlib
import urllib.parse
import json


class QiXiu:
    heartbeat = None

    @staticmethod
    async def get_ws_info(url):
        rid = url.split('/')[-1]
        s = bytes([57, 77, 83, 73, 53, 86, 85, 71, 50, 81, 74, 80, 66, 52, 78, 54, 68, 48, 81,
                   83, 89, 87, 69, 72, 67, 90, 83, 75, 84, 49, 77, 50, 84, 65, 75, 88]).decode('utf-8')
        # ua = 'User-Agent'
        # ak = deviceid = md5(str(int(time.time() * 1e3)) + ua + '0000')
        ak = deviceid = '118d2ae703e62992263e6741afbb5627'
        e = {
            'ag': 1,
            'ak': ak,
            'at': 3,
            'd': deviceid,
            'n': 1,
            'p': 1,
            'r': rid,
            'v': '1.01.0801'
        }
        i = ''
        for k, v in e.items():
            i += '{}={}|'.format(k, str(v))
        e['sg'] = hashlib.md5((i + s).encode('utf-8')).hexdigest()
        ws_url = 'ws://qx-ws.iqiyi.com/ws?' + urllib.parse.urlencode(e)
        return ws_url, None

    @staticmethod
    def decode_msg(data):
        message = json.loads(data)
        msgs = []
        msg = {'name': '', 'content': '', 'msg_type': 'other'}
        for ms in message:
            m = ms['ct']
            type_ = ms['t']
            # 200001：进场消息
            # 300001：聊天信息
            # 102001：礼物
            # 1100002：礼物
            # 400001：人气值
            # 5000010：升级
            # 700095：live_score
            # 700091：排名
            # 其他：系统消息
            if type_ == 300001:
                msg['name'] = m['op_userInfo']['nick_name']
                msg['content'] = m['msg']
                msg['msg_type'] = 'danmaku'
            elif type_ == 102001:
                msg['name'] = m['op_userInfo']['nick_name']
                num = m['op_info']['num']
                gift = m['op_info']['name']
                msg['content'] = '送出{}个{}'.format(num, gift)
                msg['msg_type'] = 'danmaku'
            elif type_ in [200001, 1100002, 110001, 3019, 3022, 3002, 3024]:
                msg['name'] = 'SYS'
                info = m['op_info'].get('public_chat_msg', 0)
                if not info:
                    info = m['op_info']['roll_chat_msg']
                content = ''
                items = info['items']
                for item in items:
                    content += item.get('content', '')
                msg['content'] = content
                msg['msg_type'] = 'danmaku'
            msgs.append(msg.copy())
            return msgs
