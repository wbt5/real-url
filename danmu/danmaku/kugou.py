from . import kugou_pb2 as pb
import struct
import requests


class InitKugou:

    def __init__(self):
        self.MAGIC = {
            'index': 0,
            'length': 1,
            'value': 100
        }
        self.VERSION = {
            'index': 1,
            'length': 2,
            'value': 1
        }
        self.TYPE = {
            'index': 2,
            'length': 1,
            'value': 1
        }
        self.HEADER = {
            'index': 3,
            'length': 2,
            'value': 12
        }
        self.CMD = {
            'index': 4,
            'length': 4,
            'value': 0
        }
        self.PAYLOAD = {
            'index': 5,
            'length': 4,
            'value': 0
        }
        self.ATTR = {
            'index': 6,
            'length': 1,
            'value': 0
        }
        self.CRC = {
            'index': 7,
            'length': 2,
            'value': 0
        }
        self.SKIP = {
            'index': 8,
            'length': 1,
            'value': 0
        }

        self.f = [self.MAGIC, self.VERSION, self.TYPE, self.HEADER,
                  self.CMD, self.PAYLOAD, self.ATTR, self.CRC, self.SKIP]

    def reg(self, rid):
        url = 'https://fx2.service.kugou.com/socket_scheduler/pc/v2/address.jsonp'
        payload = {
            'rid': rid,
            '_v': '7.0.0',
            '_p': 0,
            'pv': 20191231,
            'at': 102,
            'cid': 105
        }

        with requests.Session() as s:
            r = s.get(url, params=payload).json()
            soctoken = r['data']['soctoken']

        reg_data = {
            'appid': 1010,
            'clientid': 105,
            'cmd': 201,
            'deviceNo': '4edc0e89-ccaf-452c-bce4-00f4cb6bb5bb',
            'kugouid': 0,
            'platid': 18,
            'referer': 0,
            'roomid': rid,
            'sid': '8b9b79a7-a742-4397-fcc0-94efa3a1c920',
            'soctoken': soctoken,
            'v': 20191231
        }

        a = pb.LoginRequest()
        for k, v in reg_data.items():
            setattr(a, k, v)
        b = pb.Message()
        b.content = a.SerializeToString()
        e = b.SerializeToString()
        reg = self.encode_(e, reg_data['cmd'])
        return reg

    def g(self, *e):
        if len(e) > 1 and e[1]:
            t = e[1]
        else:
            t = 12
        n = 0
        i = 0
        e = e[0]
        while i < e and i < len(self.f):
            n += self.f[i]['length']
            i += 1
        if e == len(self.f):
            return n + t - 12
        else:
            return n

    def encode_(self, e, t):
        n = len(self.f)
        i = len(e)
        # r = self.g(n) + i
        self.PAYLOAD['value'] = i
        self.CMD['value'] = t

        buf = b''
        for s in self.f:
            # offset = self.g(s['index'])
            value = s['value']
            if s['length'] == 1:
                fmt = '!b'
            elif s['length'] == 2:
                fmt = '!h'
            else:
                fmt = '!i'
            buf += struct.pack(fmt, value)

        buf += struct.pack('!i', i)
        buf = buf[:self.g(n)] + e
        return buf

    def v(self, e, t):
        if t['length'] == 1:
            fmt = '!b'
        elif t['length'] == 2:
            fmt = '!h'
        else:
            fmt = '!i'
        r, = struct.unpack_from(fmt, e, self.g(t['index']))
        return r

    # def k(self, e, i, o=False):
    #     if i == 1:
    #         a = zlib.decompress(e)
    #     elif i == 2:
    #         a = zlib.decompress(e)
    #     else:
    #         a = e
    #     if o:
    #         return self.r(a)
    #     else:
    #         return a
    #
    # def r(self, e):
    #     pass

    def decode_(self, message):
        t = len(message)
        n = len(self.f)

        if t <= 0:
            return {}

        if self.v(message, self.TYPE) == 0:
            return {}

        r = self.v(message, self.HEADER)
        cmd = self.v(message, self.CMD)  # cmd
        a = self.g(n, r)

        if t < a:
            return {}

        o = message[a:]  # payloadBuffer

        if not o or not cmd:
            return

        msgs = []
        msg = {'name': '', 'content': '', 'msg_type': 'other'}
        if cmd == 201 or cmd == 501:
            # CMD
            # 201:LoginResponse,欢迎信息;
            # 501:ChatResponse,聊天信息;
            # 602:ContentMessage,礼物信息；
            # 901:ErrorResponse;
            s = pb.Message()
            s.ParseFromString(o)
            if s.codec == 1:
                # if s.compression:
                #     s.content = self.k(s.content, s.compression)
                s1 = pb.ContentMessage()
                s1.ParseFromString(s.content)
                if s1.codec == 1:
                    # if hasattr(s1, 'compression'):
                    #     s1.content = self.k(s1.content, s1.compression)
                    s2 = pb.ChatResponse()
                    s2.ParseFromString(s1.content)
                    if cmd == 201:
                        msg['name'] = 'SYS'
                        msg['content'] = s2.receivername.replace('%nick', s2.chatmsg)
                        msg['msg_type'] = 'danmaku'
                    elif cmd == 501:
                        msg['name'] = s2.sendername
                        msg['content'] = s2.chatmsg
                        msg['msg_type'] = 'danmaku'
        msgs.append(msg.copy())
        return msgs


class KuGou:
    heartbeat = b'\x64\x00\x01\x00'
    wss_url = 'wss://chat1wss.kugou.com/acksocket'
    heartbeatInterval = 10
    s = InitKugou()

    @staticmethod
    async def get_ws_info(url):
        rid = url.split('/')[-1]
        reg_data = KuGou.s.reg(int(rid))
        return KuGou.wss_url, [reg_data]

    @staticmethod
    def decode_msg(data):
        msgs = KuGou.s.decode_(data)
        return msgs
