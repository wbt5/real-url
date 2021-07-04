import aiohttp
import struct
import json
import re


class eGame:
    heartbeat = b'\x00\x00\x00\x12\x00\x12\x00\x01\x00\x07\x00\x00\x00\x01\x00\x00\x00\x00'
    heartbeatInterval = 60

    @staticmethod
    async def get_ws_info(url):
        rid = url.split('/')[-1]
        page_id = aid = rid
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        }
        async with aiohttp.ClientSession() as session:

            async with session.get('https://m.egame.qq.com/live?anchorid' + rid, headers=headers) as resp:
                res = await resp.text()
                res_ = re.findall(r'"videoInfo":(.*),"h5Url"', res)[0]
                str_id = json.loads(res_)['pid']
                params = {
                    'param': json.dumps({"0":{"module":"pgg.ws_token_go_svr.DefObj","method":"get_token","param":{"scene_flag":16,"subinfo":{"page":{"scene":1,"page_id":int(page_id),"str_id":str(str_id),"msg_type_list":[1,2]}},"version":1,"message_seq":-1,"dc_param":{"params":{"info":{"aid":aid}},"position":{"page_id":"QG_HEARTBEAT_PAGE_LIVE_ROOM"},"refer":{}},"other_uid":0}}})
                }

            async with session.post('https://share.egame.qq.com/cgi-bin/pgg_async_fcgi', data=params, headers=headers) as resp:
                res = json.loads(await resp.text())
                token = res['data']['0']['retBody']['data']['token']
                # 开始拼接reg_datas
                reg_datas = []
                tokenbuf = token.encode('ascii')
                bodybuf = struct.pack('!Bi', 7, len(tokenbuf)) + tokenbuf
                headerbuf = struct.pack('!ihhhihh', 18 + len(bodybuf), 18, 1, 1, 0, 0, 0)
                data = headerbuf + bodybuf
                reg_datas.append(data)
                reg_datas.append(eGame.heartbeat)

        return 'wss://barragepush.egame.qq.com/sub', reg_datas

    @staticmethod
    def decode_msg(data):
        """
        type: 0、3、9用户发言；7、33礼物信息；29、35欢迎信息；24、31系统提醒；23关注信息
        """
        msgs = []
        msg = {}
        s = MessageDecode(data)
        body = s.v()['body']
        if body:
            bin_datas = body['bin_data']
            for bin_data in bin_datas:
                # if bin_data['type'] in (0, 3, 9):
                if bin_data.get('type', '') in (0, 3, 9):
                    msg['name'] = bin_data['nick']
                    msg['content'] = bin_data['content']
                    msg['msg_type'] = 'danmaku'
                else:
                    msg = {'name': '', 'content': '', 'msg_type': 'other'}
                msgs.append(msg.copy())
            return msgs
        else:
            msg = {'name': '', 'content': '', 'msg_type': 'None'}
        msgs.append(msg.copy())
        return msgs


class MessageDecode:
    """
    数据解包，还原JS中的操作步骤
    """

    def __init__(self, data):

        self.data = data

        self.ie = {
            'event_id': 0,
            'msg_type': 1,
            'bin_data': 2,
            'params': 3,
            'start_tm': 4,
            'data_list': 6,
            'end_tm': 5,
            'message_seq': 7,
        }

        self.ne = {
            'uid': 0,
            'msgid': 1,
            'nick': 2,
            'content': 3,
            'tm': 4,
            'type': 5,
            'scenes_flag': 6,
            'ext': 7,
            'send_scenes': 8
        }

        self.oe = {
            'event_id': 0,
            'event_name': 1,
            'info': 2,
            'params': 3,
            'bin_data': 4
        }

    def v(self):
        data = self.data
        startPosition = 18
        endPosition, = struct.unpack_from('!i', data, 0)
        seq, = struct.unpack_from('!i', data, 10)
        operation, = struct.unpack_from('!h', data, 8)

        if endPosition != len(data):
            raise Exception('The received packet length is abnormal')

        return {
            'seq': seq,
            'operation': operation,
            'body': self.w(operation, startPosition, endPosition, data)
        }

    def w(self, operation, startPosition, endPosition, data):
        if operation == 3:
            return self.x(startPosition, endPosition, data)
        else:
            return None

    def x(self, startPosition, endPosition, data):
        i, = struct.unpack_from('!i', data, startPosition)
        n = data[startPosition: endPosition]
        if len(n) >= (4 + i):
            o = n[4:(4 + i)]
            a = self.S(o)
            y = self.ye(a)
            return y
        else:
            return None

    def ye(self, e):
        return self.T({
            'resultObj': e,
            'template': self.ie,
            'afterChange': 1,

        })

    def afterChange(self, e, t, i, n, o):
        if t == 'bin_data':
            v = []
            ve = {}
            for m in n:
                a = self.S(e, m['ext'])
                b = o['msg_type']
                if b == 1:
                    ve = self.T({
                        'resultObj': a,
                        'template': self.ne
                    })
                elif b == 2:
                    ve = self.T({
                        'resultObj': a,
                        'template': self.oe
                    })
                v.append(ve.copy())
            return v
        else:
            return n

    def T(self, e):
        i = e['resultObj']
        n = e['template']
        o = e.get('beforeChange', '')
        r = e.get('afterChange', '')
        a = {}
        for s in n.keys():
            for t in i[0]:
                if t['tag'] == n[s]:
                    q = t
                    p = q['value']
                    c = q['ext']
                    if r:
                        a[s] = self.afterChange(i[1], s, c, p, a)
                    else:
                        a[s] = p
                    break
        return a

    def S(self, e, t=0):
        if t == '':
            t = 0
        i = []
        n = len(e)
        while t < n:
            o = self.m(e, t)
            dict_ = {
                'value': o['value'],
                'lastPosition': o['position'],
                'ext': o['ext'],
                'tag': o['tag']
            }
            i.append(dict_.copy())
            t = o['position']
        return i, e

    def m(self, e, t):
        value = position = ext = ''
        i = e
        a, = struct.unpack_from('!B', i, t)
        tag = (240 & a) >> 4
        type = 15 & a
        s_position = t + 1

        if type == 0:
            value, position = self.f0(i, s_position)
        elif type == 1:
            value, position = self.f1(i, s_position)
        elif type == 2:
            value, position = self.f2(i, s_position)
        elif type == 3:
            value, position = self.f3(i, s_position)
        elif type == 6:
            value, position, ext = self.f6(i, s_position)
        elif type == 7:
            value, position, ext = self.f7(i, s_position)
        elif type == 8:
            value, position = self.f8(i, s_position)
        elif type == 9:
            value, position = self.f9(i, s_position)
        elif type == 12:
            value, position = self.f12(i, s_position)
        elif type == 13:
            value, position = self.f13(i, s_position)

        i = ''

        return {
            'i': i,
            'tag': tag,
            'type': type,
            'value': value,
            'position': position,
            'ext': ext
        }

    def f0(self, e, t):
        o = 1
        try:
            n, = struct.unpack_from('!B', e, t)
        except:
            n = ''
        return n, t + o

    def f1(self, e, t):
        o = 2
        try:
            n, = struct.unpack_from('!H', e, t)
        except:
            n = ''
        return n, t + o

    def f2(self, e, t):
        o = 4
        try:
            n, = struct.unpack_from('!I', e, t)
        except:
            n = ''
        return n, t + o

    def f3(self, e, t):
        e = struct.unpack('!8B', e[t:t + 8])
        i = (e[0] << 24) + (e[1] << 16) + (e[2] << 8) + e[3]
        o = (e[4] << 24) + (e[5] << 16) + (e[6] << 8) + e[7]
        value = (i << 32) + o
        position = t + 8
        return value, position

    def f4(self, e, t):
        o = 4
        try:
            n, = struct.unpack_from('!f', e, t)
        except:
            n = ''
        return n, t + o

    def f5(self, e, t):
        o = 8
        try:
            n, = struct.unpack_from('!d', e, t)
        except:
            n = ''
        return n, t + o

    def f6(self, e, t):
        n, = struct.unpack_from('!B', e, t)
        r = t + 1
        s = r + n
        value = (e[r:s]).decode('utf8', errors='ignore')
        return value, s, r

    def f7(self, e, t):
        n, = struct.unpack_from('!I', e, t)
        r = t + 4
        s = r + n
        value = (e[r:s]).decode('utf8', errors='ignore')
        return value, s, r

    def f8(self, e, t):
        i = {}
        b = self.m(e, t)
        o = b['value']
        r = b['position']
        while o > 0:
            a = self.m(e, r)
            s = self.m(e, a['position'])
            if a['tag'] == 0 and s['tag'] == 1:
                i[a['value']] = s['value']
            r = s['position']
            o -= 1
        return i, r

    def f9(self, e, t):
        i = self.m(e, t)
        n = i['value']
        o = i['position']
        r = []
        while n > 0:
            a = self.m(e, o)
            r.append(a.copy())
            o = a['position']
            n -= 1
        return r, o

    def f10(self, e, t):
        i = []
        while True:
            n = self.m(e, t)
            t = n['position']
            if n['type'] == 11:
                return i, t
            i.append(n['value'].copy())

    def f11(self, e, t):
        return '', t

    def f12(self, e, t):
        return 0, t

    def f13(self, e, t):
        i = self.m(e, t)
        return e[(t + i['position']):i['value']], t + i['position'] + i['value']
