import binascii
import struct

import requests
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad

from . import yqs_pb2 as pb


class YiQiShan:
    ws_url = 'wss://websocket.173.com/'

    def __init__(self, rid):
        self.rid = str(rid)
        self.key = b'e#>&*m16'
        with requests.Session() as se:
            res = se.get('http://www.173.com/{}'.format(rid))
            try:
                self.uuid, _, token, _ = res.cookies.values()
            except ValueError:
                raise Exception('房间不存在')
        self.accesstoken = binascii.a2b_hex(token)
        s = YiQiShan.des_decode(self.accesstoken, self.key)
        p = pb.Token()
        p.ParseFromString(s)
        self.gtkey = p.gtkey[:8]

    @staticmethod
    def des_encode(t, key):
        t = pad(t, DES.block_size)
        c = DES.new(key, DES.MODE_ECB)
        res = c.encrypt(t)
        return res

    @staticmethod
    def des_decode(t, key):
        c = DES.new(key, DES.MODE_ECB)
        res = c.decrypt(t)
        length = len(res)
        padding = res[length - 1]
        res = res[0:length - padding]
        return res

    def startup(self):
        p = pb.TCPAccessReq()
        p.AccessToken = self.accesstoken
        return p.SerializeToString()

    def tcphelloreq(self):
        p = pb.TcpHelloReq()
        p.uuid = self.uuid
        return p.SerializeToString()

    def enterroomreq(self):
        p = pb.EnterRoomReq()
        p.uuid = self.uuid.encode()
        p.roomid = self.rid.encode()
        return p.SerializeToString()

    def roomhelloreq(self):
        p = pb.RoomHelloReq()
        p.uuid = self.uuid.encode()
        p.roomid = self.rid.encode()
        return p.SerializeToString()

    def pack(self, paylod_type):
        command = {
            'startup': 123,
            'tcphelloreq': 122,
            'enterroomreq': 601,
            'roomhelloreq': 600
        }
        subcmd = {
            'startup': 0,
            'tcphelloreq': 0,
            'enterroomreq': 1,
            'roomhelloreq': 1
        }
        p = pb.CSHead()
        p.command = command[paylod_type]
        p.subcmd = subcmd[paylod_type]
        p.uuid = self.uuid.encode()
        p.clientType = 4
        p.routeKey = int(self.rid)
        n = p.SerializeToString()

        key = self.key if paylod_type == 'startup' else self.gtkey
        payload = getattr(self, paylod_type)()
        s = YiQiShan.des_encode(payload, key)

        buf = struct.pack('!HcH', len(n) + len(s) + 8, b'W', len(n))
        buf += n
        buf += struct.pack('!H', len(s))
        buf += s + b'M'
        return buf

    def unpack(self, data):
        msgs = [{'name': '', 'content': '', 'msg_type': 'other'}]

        s, = struct.unpack_from('!h', data, 3)
        p, = struct.unpack_from('!h', data, 5 + s)
        u = data[7 + s:7 + s + p]

        a = pb.CSHead()
        a.ParseFromString(data[5:5 + s])
        cmd = a.command
        key = self.key if cmd == 123 else self.gtkey
        t = u if cmd == 102 else YiQiShan.des_decode(u, key)

        o = cmd
        # r = a.subcmd
        if o == 102:
            p = pb.SendBroadcastPkg()
            p.ParseFromString(t)
            for i in p.broadcastmsg:
                # PublicChatNotify = 1
                # BUSINESS_TYPE_FREE_GIFT = 2
                # BUSINESS_TYPE_PAY_GIFT = 3
                if i.businesstype == 1:  # 发言
                    q = pb.PublicChatNotify()
                    q.ParseFromString(i.content)
                    user = q.nick.decode()
                    content = q.info.textmsg.decode()
                # elif i.businesstype == 2: # 免费礼物
                #     print(i.businesstype)
                #     q = pb.NotifyFreeGift()
                #     q.ParseFromString(i.content)
                # elif i.businesstype == 3: # 收费礼物
                #     print(i.businesstype)
                #     q = pb.GiftNotyInfo()
                #     q.ParseFromString(i.content)
                # else:
                #     pass
                    msg = {'name': user, 'content': content, 'msg_type': 'danmaku'}
                    msgs.append(msg.copy())
        return msgs
