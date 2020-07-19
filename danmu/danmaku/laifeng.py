import aiohttp
import json
import time


class LaiFeng:
    heartbeat = '2::'
    heartbeatInterval = 30

    @staticmethod
    async def get_ws_info(url):
        rid = url.split('/')[-1]
        async with aiohttp.ClientSession() as session:
            async with session.get('http://v.laifeng.com/') as resp:
                imk = dict(resp.cookies)['imk'].value
        args = {
            'name': 'enter',
            'args': [{
                'token': imk.replace('%3D', '='),
                'yktk': '',
                'uid': '2082628924',
                'isPushHis': '1',
                'roomid': rid,
                'endpointtype': 'ct_,dt_1_1003|0|_{}|CTaXF+oKpB4CAatxtZHBQchJ'.format(time.time() * 1e3)
            }]
        }
        reg_data = '5:::' + json.dumps(args)
        return 'ws://normal01.chatroom.laifeng.com/socket.io/1/websocket/', [reg_data]

    @staticmethod
    def decode_msg(message):
        type_ = message[0]
        msgs = []
        msg = {'name': '', 'content': '', 'msg_type': 'other'}
        if type_ == '5':
            data = json.loads(message[4:])
            name = data.get('name', 0)
            args = data['args']
            for arg in args:
                if name == 'enterMessage':  # 入场信息
                    msg['name'] = 'SYS'
                    msg['content'] = arg['body']['n'] + ' 进入频道'
                    msg['msg_type'] = 'danmaku'
                elif name == 'globalHornMessage':  # 系统消息
                    msg['name'] = 'SYS'
                    msg['content'] = arg['body']['m']
                    msg['msg_type'] = 'danmaku'
                elif name == 'chatMessage':  # 弹幕
                    msg['name'] = arg['body']['n']
                    msg['content'] = arg['body']['m']
                    msg['msg_type'] = 'danmaku'
                msgs.append(msg.copy())
        return msgs
