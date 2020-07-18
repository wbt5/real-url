import aiohttp
import json
import time


class QF:
    heartbeat = '2::'
    heartbeatInterval = 30

    @staticmethod
    async def get_ws_info(url):
        rid = url.split('/')[-1]
        async with aiohttp.ClientSession() as session:
            async with session.get('https://conn-chat.qf.56.com/socket.io/1/') as resp:
                res = await resp.text()
                sessid = res.split(':')[0]
                ws_url = 'wss://conn-chat.qf.56.com/socket.io/1/websocket/' + sessid
                # e = 2
                t = 'connector-sio.entryHandler.enter'
                s = {
                    'userId': '',
                    'aq': 0,
                    'roomId': rid,
                    'token': '',
                    'ip': '',
                    'recet': 0,
                    'params': {
                        'referFrom': '0'
                    },
                    'apType': 0,
                    'timestamp': int(time.time() * 1e3)
                }
                r = json.dumps(s, separators=(',', ':'))
                if len(t) > 255:
                    raise Exception('route maxlength is overflow')
                reg_data = '3:::' + '\x00\x00\x00\x02 ' + t + r
        return ws_url, [reg_data]

    @staticmethod
    def decode_msg(message):
        msgs = []
        msg = {'name': '', 'content': '', 'msg_type': 'other'}
        type_ = message[0]
        if type_ == '3':
            data = json.loads(message[4:])
            route = data.get('route', 0)
            body = data['body']
            if route == 'onUserLog':  # 入场信息
                msg['name'] = 'SYS'
                msg['content'] = body['userName'] + ' 来了'
                msg['msg_type'] = 'danmaku'
            elif route == 'onChat':  # 弹幕
                msg['name'] = body['userName']
                msg['content'] = body['content']
                msg['msg_type'] = 'danmaku'
            elif route == 'onGift':  # 弹幕
                msg['name'] = 'SYS'
                msg['content'] = body['userName'] + ' 送礼物 ' + body['giftName']
                msg['msg_type'] = 'danmaku'
            elif route == 'onBc':  # 弹幕
                msg['name'] = 'SYS'
                msg['content'] = body['userName'] + '：' + body['msg']
                msg['msg_type'] = 'danmaku'
        msgs.append(msg.copy())
        return msgs
