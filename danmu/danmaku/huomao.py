import struct
import aiohttp
import json


class HuoMao:
    heartbeat = b'\x00\x00\x00\x10\x00\x10\x00\x01\x00\x00\x00\x02\x00\x00\x00\x01'
    # heartbeat = struct.pack('!ihhii', 16,16,1,2,1)
    heartbeatInterval = 30

    @staticmethod
    async def get_ws_info(url):
        goim = 'http://www.huomao.com/ajax/goimConf?type=h5'
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, '
                          'like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'}
        async with aiohttp.ClientSession() as session:
            async with session.get(goim, headers=headers) as resp:
                info = json.loads(await resp.text())
                webSocketUrls = info.get('host_wss', 0)
                rid = int(url.split('/')[-1])
                reg_datas = []
                tokenBody = json.dumps({"Uid": 0, "Rid": rid}, separators=(',', ':'))
                bodyBuf = tokenBody.encode('ascii')
                headerBuf = struct.pack('!ihhii', (16 + len(bodyBuf)), 16, 1, 7, 1)
                data = headerBuf + bodyBuf
                reg_datas.append(data)
        return webSocketUrls, reg_datas

    @staticmethod
    def decode_msg(data):
        packetLen, headerLen, ver, op, seq = struct.unpack('!ihhii', data[0:16])
        msgs = []
        msg = {'name': '', 'content': '', 'msg_type': 'other'}
        if op == 5:
            offset = 0
            while offset < len(data):
                packetLen, headerLen, ver = struct.unpack('!ihh', data[offset:(offset + 8)])
                msgBody = data[offset + headerLen:offset + packetLen]
                offset += packetLen
                body = json.loads(msgBody.decode('utf8'))
                if body.get('code', 0) == '100001':
                    msg['name'] = body['speak']['user']['name']
                    msg['content'] = body['speak']['barrage']['msg']
                    msg['msg_type'] = 'danmaku'
                    msgs.append(msg.copy())
            return msgs
        msgs.append(msg)
        return msgs
