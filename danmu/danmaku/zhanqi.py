import json
import struct
import aiohttp


class ZhanQi:
    heartbeat = b'\xbb\xcc\x00\x00\x00\x00\x15\x00\x00\x00\x10\'{"cmdid": "keeplive"}'
    wss_url = 'wss://gw.zhanqi.tv/'
    heartbeatInterval = 30

    @staticmethod
    async def get_ws_info(url):
        reg_datas = []
        rid = url.split('/')[-1]
        async with aiohttp.ClientSession() as session:
            async with session.get('https://m.zhanqi.tv/api/static/v2.1/room/domain/{}.json'.format(rid)) as resp:
                info = json.loads(await resp.text())
                roomid = info['data']['id']
            async with session.get('https://m.zhanqi.tv/api/public/room.viewer') as resp2:
                res = json.loads(await resp2.text())
                gid = res['data']['gid']
                sid = res['data']['sid']
                timestamp = res['data']['timestamp']

        login = {
            'cmdid': 'loginreq',
            'roomid': int(roomid),
            'chatroomid': 0,
            'gid': gid,
            'sid': sid,
            't': 0,
            'r': 0,
            'device': 1,
            'fhost': 'mzhanqi',
            'uid': 0,
            'timestamp': timestamp
        }
        body = json.dumps(login, separators=(',', ':'))
        head = struct.pack('<HIIH', 0xCCBB, 0, len(body), 10000)
        reg_data = head + body.encode()
        reg_datas.append(reg_data)
        return ZhanQi.wss_url, reg_datas

    @staticmethod
    def decode_msg(message):
        message = (message[12:])
        data = json.loads(message)
        msgs = []
        msg = {'name': '', 'content': '', 'msg_type': 'other'}
        if data['cmdid'] == 'chatmessage':  # 聊天信息
            msg['name'] = data['fromname']
            msg['content'] = data['content']
            msg['msg_type'] = 'danmaku'
        elif data['cmdid'] == 'Gift.Display':  # 礼物信息
            pass
        elif data['cmdid'] == 'Prop.Display':  # 礼物信息
            pass
        elif data['cmdid'] == 'getuc':  # 人气数
            pass
        elif data['cmdid'] == 'loginresp':  # 欢迎信息
            pass
        msgs.append(msg.copy())
        return msgs
