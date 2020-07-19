import aiohttp
import time
import uuid
import struct
import math
import zlib
import json
import re


class CC_Init:
    def __init__(self):
        self.offset = 0

    def get_reg(self):
        sid = 6144
        cid = 2
        update_req_info = {
            '22': 640,
            '23': 360,
            '24': "web",
            '25': "Linux",
            '29': "163_cc",
            '30': "",
            '31': "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Mobile Safari/537.36"
        }
        macAdd = device_token = str(uuid.uuid1()) + '@web.cc.163.com'
        data = {
            'web-cc': int(time.time() * 1e3),
            'macAdd': macAdd,
            'device_token': device_token,
            'page_uuid': str(uuid.uuid1()),
            'update_req_info': update_req_info,
            'system': 'win',
            'memory': 1,
            'version': 1,
            'webccType': 4253
        }
        reg_data = struct.pack('<HHI', sid, cid, 0) + self.encode_dict(data)
        return reg_data

    def get_beat(self):
        sid = 6144
        cid = 5
        data = {}
        beat_data = struct.pack('<HHI', sid, cid, 0) + self.encode_dict(data)
        return beat_data

    def get_join(self, data_cid, data_gametype, data_roomId):
        sid = 512
        cid = 1
        data = {
            'cid': data_cid,
            'gametype': data_gametype,
            'roomId': data_roomId
        }
        join_data = struct.pack('<HHI', sid, cid, 0) + self.encode_dict(data)
        return join_data

    def encode_str(self, r):
        n = len(r)
        i = 5 + 3 * n
        s = f = 1 if n < 32 else 2 if n <= 255 else 3 if n <= 65535 else 5
        b = 160 + n if s == 1 else 215 + s if s <= 3 else 219
        if f == 1:
            e = bytes([b])
        else:
            e = bytes([b, n])
        return e + r.encode()

    def encode_num(self, e):
        if e <= 255:
            return struct.pack('!B', e)
        if 255 < e <= 65535:
            t = struct.pack('!H', e)
            return b'\xcd' + t
        else:
            t = []
            r = 9
            n = 0
            i = 52
            o = 8
            s = 8 * o - i - 1
            c = (1 << s) - 1
            h = c >> 1
            l = pow(2, -24) - pow(2, -77) if i == 23 else 0
            d = 0 if n else o - 1
            p = 1 if n else -1
            y = 1 if (e < 0 or e == 0 and 1 / e) else 0

            while i >= 8:
                e = abs(e)
                f = math.floor(math.log(e) / math.log(2))
                u = pow(2, -1 * f)
                if e * u < 1:
                    f -= 1
                    u *= 2
                if f + h >= 1:
                    e += l / u
                else:
                    e += l * pow(2, 1 - h)
                if e * u >= 2:
                    f += 1
                    u /= 2
                if f + h >= c:
                    a = 0
                    f = c
                elif f + h >= 1:
                    a = (e * u - 1) * pow(2, i)
                    f += h
                else:
                    a = e * pow(2, h - 1) * pow(2, i)
                    f = 0

                t.append(255 & int(a))
                d += p
                a /= 256
                i -= 8

            f = f << i | int(a)
            s += i
            while s > 0:
                t.append(255 & int(f))
                d += p
                f /= 256
                s -= 8

            t[-1] |= 128 * y

            t.reverse()
            return b'\xcb' + bytes(t)

    def encode_dict(self, d):
        n = len(d)
        r = 128 + n if n < 16 else 222 if n <= 65535 else 223
        t = bytes([r])
        for k, v in d.items():
            t += self.encode_str(k)
            if isinstance(v, int):
                t += self.encode_num(v)
            elif isinstance(v, str):
                t += self.encode_str(v)
            elif isinstance(v, dict):
                t += self.encode_dict(v)
        return t

    def p(self, fmt):
        def r(t):
            s, = struct.unpack_from(fmt, t, self.offset)
            self.offset += struct.calcsize(fmt)
            return s

        return r

    def i(self, t):
        return lambda t: int(t[self.offset - 1])

    def o(self, t, e):
        return lambda r: e(r, t(r))

    def f(self, t, e):
        return lambda r: e(r, t)

    def n(self, e):
        if 0 <= e <= 127:
            r = self.i(e)
        elif 128 <= e <= 143:
            r = self.f(e - 128, self.de_dict)
        elif 144 <= e <= 159:
            r = self.f(e - 144, self.de_list)
        elif 160 <= e <= 191:
            r = self.f(e - 160, self.de_str)
        elif e == 192:
            r = self.i(None)
        elif e == 193:
            r = None
        elif e == 194:
            r = self.i(False)
        elif e == 195:
            r = self.i(True)
        elif e == 202:
            r = self.p('>f')
        elif e == 203:
            r = self.p('>d')
        elif e == 204:
            r = self.p('>B')
        elif e == 205:
            r = self.p('>H')
        elif e == 206:
            r = self.p('>I')
        elif e == 207:
            r = self.p('>Q')
        elif e == 208:
            r = self.p('>b')
        elif e == 209:
            r = self.p('>h')
        elif e == 210:
            r = self.p('>i')
        elif e == 211:
            r = self.p('>q')
        elif e == 217:
            r = self.o(self.p('>B'), self.de_str)
        elif e == 218:
            r = self.o(self.p('>H'), self.de_str)
        elif e == 219:
            r = self.o(self.p('>I'), self.de_str)
        elif e == 220:
            r = self.o(self.p('>H'), self.de_list)
        elif e == 221:
            r = self.o(self.p('>I'), self.de_list)
        elif e == 222:
            r = self.o(self.p('>H'), self.de_dict)
        elif e == 223:
            r = self.o(self.p('>I'), self.de_dict)
        elif 224 <= e <= 256:
            r = self.i(e - 256)
        return r

    def de_init(self, t):
        r = int(t[self.offset])
        self.offset += 1
        n = self.n(r)
        return n(t)

    def de_str(self, t, e):
        s = t[self.offset: self.offset + e].decode('utf-8')
        self.offset += e
        return s

    def de_list(self, t, e):
        l = [''] * e
        n = self.de_init
        for i in range(e):
            l[i] = n(t)
        return l

    def de_dict(self, t, e):
        k = [''] * e
        v = [''] * e
        f = self.de_init
        for r in range(e):
            k[r] = f(t)
            v[r] = f(t)
        d = dict(zip(k, v))
        return d


class CC:
    s = CC_Init()

    heartbeatInterval = 30
    heartbeat = s.get_beat()

    @staticmethod
    async def get_ws_info(url):
        cid = re.search(r'com/(\d+)/', url).group(1)
        url = 'https://api.cc.163.com/v1/activitylives/anchor/lives?anchor_ccid=' + str(cid)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                res = await resp.text()
                data = json.loads(res).get('data').get(cid)
                channel_id = data['channel_id']
                roomId = data['room_id']
                gametype = data['gametype']

                reg_data = CC.s.get_reg()
                beat_data = CC.s.get_beat()
                join_data = CC.s.get_join(channel_id, gametype, roomId)
        reg_datas = (reg_data, beat_data, join_data)
        return 'wss://weblink.cc.163.com/', reg_datas

    @staticmethod
    def decode_msg(e):
        n, r, p = struct.unpack('<HHI', e[:8])
        i = 'tcp-{}-{}'.format(n, r)
        studio = {
            'tcp-512-32784': 'origin',
            'tcp-515-32785': 'chat',
            'tcp-535-32769': 'gamechat'
        }
        # 进场协议：tcp-512-32784
        # 聊天协议：tcp-515-32785
        # 游戏聊天：tcp-535-32769
        msgs = []
        if i in studio.keys():
            if p:
                s, = struct.unpack('<I', e[8:12])
                a = e[12:]
                if len(a) == s:
                    o = a
            else:
                o = e[8:]
            o = o if int(o[0]) != 120 else zlib.decompress(o)
            CC.s.offset = 0
            msg = CC.s.de_init(o)

            ms_type = studio[i]

            if ms_type == 'origin':
                ms = msg['data']['msg_list']
            else:
                ms = msg['msg']

            for m in ms:
                if ms_type == 'origin':
                    name = m['name']
                    content = '欢迎来到直播间'
                elif ms_type == 'chat':
                    name = m[197]
                    content = m[4]
                elif ms_type == 'gamechat':
                    name = json.loads(m[7])['nickname']
                    content = m[4]
                msg = {'name': name, 'content': content, 'msg_type': 'danmaku'}
                msgs.append(msg.copy())
        else:
            msgs = [{'name': '', 'content': '', 'msg_type': 'other'}]
        return msgs
