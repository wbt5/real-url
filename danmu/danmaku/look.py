from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import aiohttp
import json
import base64


class Look:
    heartbeat = '2::'
    heartbeatInterval = 30

    @staticmethod
    def aes_(t, key):
        t = t.encode('utf-8')
        t = pad(t, AES.block_size)
        key = key.encode()
        iv = b'0102030405060708'
        mode = AES.MODE_CBC
        c = AES.new(key, mode, iv)
        res = c.encrypt(t)
        return base64.b64encode(res).decode('utf-8')

    @staticmethod
    async def get_ws_info(url):
        rid = url.split('=')[-1]
        async with aiohttp.ClientSession() as session:
            async with session.get('https://weblink10.netease.im/socket.io/1/') as resp:
                res = await resp.text()
                sessid = res.split(':')[0]
            ws_url = 'wss://weblink10.netease.im/socket.io/1/websocket/' + sessid
            room = {
                'liveRoomNo': rid
            }
            c = json.dumps(room, separators=(',', ':'))
            data = {
                'params': Look.aes_(Look.aes_(c, '0CoJUm6Qyw8W8jud'), 'dV00kZnm4Au69cp2'),
                'encSecKey': 'e08bda29630b9a9bbf9552a1e5f889972aedfe6bc4e695b60d566294043431c60e42487153c6e0df42df0aa9d40c739552d8d8ee58d9acbcab8f4ae0df997a787eefcc56bdcd12fd2f1e41bdb5f9db240b3e10b6bd762fd207853af4c78dddf8254cf6ff83599120bd041c3e7dfb3faea1cd2886bd2c40de0981a11ae2af2a33 '
            }
            async with session.post('https://api.look.163.com/weapi/livestream/room/get/v3', data=data) as resp:
                res = await resp.json()
                roomid = res['data']['roomInfo']['roomId']

        args = {
            'SID': 13,
            'CID': 2,
            'SER': 1,
            'Q': [{
                't': 'byte',
                'v': 1
            }, {
                't': 'Property',
                'v': {
                    '1': '3a6a3e48f6854dfa4e4464f3bdaec3b4',
                    '2': '',
                    '3': '1713a7e3e1e4d7b99fe5bcff2fe7e178',
                    '5': roomid,
                    '8': 0,
                    '20': '',
                    '21': ' ',
                    '26': '',
                    '38': 1
                }
            }, {
                't': 'Property',
                'v': {
                    '4': '',
                    '6': '47',
                    '8': 1,
                    '9': 1,
                    '13': '1713a7e3e1e4d7b99fe5bcff2fe7e178',
                    '18': '3a6a3e48f6854dfa4e4464f3bdaec3b4',
                    '19': '',
                    '24': '',
                    '26': '',
                    '1000': ''
                }
            }
            ]
        }
        reg_data = '3:::' + json.dumps(args, separators=(',', ':'))

        return ws_url, [reg_data]

    @staticmethod
    def decode_msg(message):
        type_ = message[0]
        msgs = []
        msg = {'name': '', 'content': '', 'msg_type': 'other'}
        if type_ == '3':
            data = json.loads(message[4:])
            if data['cid'] == 10:
                body = data['r'][1]['body']
                body = body[0]
                if body['2'] == '100':
                    info = json.loads(body['4'])
                    if info['type'] == 114:  # 入场信息
                        msg['name'] = info['content']['user']['nickName']
                        msg['content'] = ' 进入了直播间'
                        msg['msg_type'] = 'danmaku'
                    elif info['type'] == 102:  # 礼物
                        msg['name'] = info['content']['user']['nickName']
                        number = info['content']['number']
                        giftname = info['content']['giftName']
                        msg['content'] = ' 送了{}{}个'.format(giftname, number)
                        msg['msg_type'] = 'danmaku'
                elif body['2'] == '0':  # 发言
                    info = json.loads(body['4'])
                    msg['name'] = info['content']['user']['nickname']
                    msg['content'] = body['3']
                    msg['msg_type'] = 'danmaku'
        msgs.append(msg.copy())
        return msgs
