from . import huajiao_pb2 as pb
import struct
import hashlib
import random
import string
import json
import time


class HuaJiao:

    heartbeat = b'\x00\x00\x00\x00'
    ws_url = 'wss://bridge.huajiao.com'

    def __init__(self, rid=None):
        self.sn = ''
        self.tt = str(int(time.time() * 1000))
        self.roomId = rid
        self.flag = 'qh'
        self.protocolVersion = 1
        self.clientVersion = 101
        self.appId = 2080
        self.sender = self.password = '999' + self.tt + self.random_(6, 'n')
        self.defaultKey = '3f190210cb1cf32a2378ee57900acf78'

    def init_p(self):
        p = pb.Message()
        p.sn = int(self.random_(10, 'n'))
        p.sender = self.sender
        p.sender_type = 'jid'
        return p

    @staticmethod
    def random_(num, var):
        seq = ''
        if var == 's':
            seq = string.ascii_letters + string.digits
        if var == 'n':
            seq = string.digits
        result = ''.join([random.choice(seq) for i in range(num)])
        return result

    @staticmethod
    def md5(data):
        return hashlib.md5(data.encode('utf-8')).hexdigest()

    @staticmethod
    def rc4(data, key):
        a = [i for i in range(256)]
        l = i = 0
        while i < 256:
            l = (l + a[i] + ord(key[i % len(key)])) % 256
            a[i], a[l] = a[l], a[i]
            i += 1
        i = l = n = 0
        s = len(data)
        f = []
        while n < s:
            i = (i + 1) % 256
            l = (l + a[i]) % 256
            a[i], a[l] = a[l], a[i]
            f.append(data[n] ^ a[(a[i] + a[l]) % 256])
            n += 1
        return bytes(f)

    def sendHandshakePack(self):
        HandshakePack = struct.pack('!2sbbhih', self.flag.encode(), self.protocolVersion << 4, self.clientVersion,
                                    self.appId, 0, 0)
        p = self.init_p()
        self.sn = p.sn
        p.msgid = 100009
        p.req.init_login_req.client_ram = self.random_(10, 's')
        p.req.init_login_req.sig = ''
        data = p.SerializeToString()
        a = self.rc4(data, self.defaultKey)
        HandshakePack += struct.pack('!i', len(HandshakePack + a) + 4) + a
        return HandshakePack

    def processHandShakePack(self, message):
        o, = struct.unpack('!2s', message[:2])
        if o.decode() != self.flag:
            raise Exception('processHandShakePack 服务器响应标识（flag）有误')
        s = self.rc4(message[6:], self.defaultKey)
        p = self.init_p()
        try:
            p.ParseFromString(s)
        except:
            raise Exception('processHandShakePack 解析消息体异常')
        if p.msgid != 200009:
            raise Exception('processHandShakePack 响应msgid异常')
        if p.sn != self.sn:
            raise Exception('processHandShakePack sn验证失败')
        return p.resp

    def sendLoginPack(self, message):
        e = self.processHandShakePack(message)
        u = e.init_login_resp.server_ram
        secret_ram = self.rc4((u + self.random_(8, 's')).encode(), self.password)
        verf_code = self.md5(self.sender + '360tantan@1408$')[24:]

        p = self.init_p()
        self.sn = p.sn
        p.msgid = 100001

        p.req.login.app_id = 2080
        p.req.login.mobile_type = 'ios'
        p.req.login.net_type = 4
        p.req.login.not_encrypt = True
        p.req.login.platform = 'h5'
        p.req.login.server_ram = u
        p.req.login.secret_ram = secret_ram
        p.req.login.verf_code = verf_code

        a = p.SerializeToString()
        l = self.rc4(a, self.defaultKey)
        LoginPack = struct.pack('!i', 4 + len(l)) + l
        return LoginPack

    def processLoginPack(self, message):
        p = self.init_p()
        try:
            p.ParseFromString(self.rc4(message[4:], self.password))
        except:
            try:
                p.ParseFromString(self.rc4(message[4:], self.defaultKey))
            except:
                raise Exception('processLoginPack 解析消息体异常')
        if p.msgid != 200001:
            raise Exception('processLoginPack 响应msgid异常')
        if p.sn != self.sn:
            raise Exception('processLoginPack sn验证失败')

        return p

    def sendJoinChatroomPack(self, message):
        p = self.processLoginPack(message)
        o = self.roomId.encode()
        # crm : ChatroomRequestMessage
        crm = pb.ChatRoomPacket()
        crm.client_sn = p.sn
        crm.roomid = o
        crm.appid = self.appId
        crm.uuid = self.md5(self.random_(10, 's') + '0000000001' + str(int(time.time() * 1000)))
        crm.to_server_data.payloadtype = 102
        crm.to_server_data.applyjoinchatroomreq.roomid = o
        crm.to_server_data.applyjoinchatroomreq.room.roomid = o
        crm.to_server_data.applyjoinchatroomreq.userid_type = 0

        p = self.init_p()
        self.sn = p.sn
        p.msgid = 100011
        p.req.service_req.service_id = 10000006
        p.req.service_req.request = crm.SerializeToString()

        u = p.SerializeToString()
        JoinChatroomPack = struct.pack('!i', 4 + len(u)) + u

        return JoinChatroomPack

    def processMessagePack(self, message):
        i, = struct.unpack_from('!i', message, 0)
        if len(message) == 4 and i == 0:  # HeartbeatPack
            return None

        p = self.init_p()
        p.ParseFromString(message[4:])
        o = p.msgid

        if o == 200011:
            return self.processService_RespMessage(p)
        elif o == 300000:
            return self.processNewMessageNotifyMessage(p)
        else:
            return None

    def processService_RespMessage(self, p):
        if p.sn != self.sn:
            raise Exception('processService_RespMessage sn验证失败')
        crp = pb.ChatRoomPacket()
        crp.ParseFromString(p.resp.service_resp.response)
        n = crp.to_user_data
        r = i = ''
        if n.payloadtype == 102 or n.applyjoinchatroomresp:
            if n.result == 0:
                r = n.applyjoinchatroomresp.room.properties[1].value
                i = n.applyjoinchatroomresp.room.partnerdata
                r = r.decode('utf-8')
                i = i.decode('utf-8')
        return r, i

    def processNewMessageNotifyMessage(self, p):
        crp = pb.ChatRoomPacket()
        crp.ParseFromString(p.notify.newinfo_ntf.info_content)
        r = crp.to_user_data
        s = i = ''
        if r.result == 0:
            if r.payloadtype == 1000 and r.newmsgnotify:
                s = r.newmsgnotify.memcount
                i = r.newmsgnotify.msgcontent
            elif r.payloadtype == 1001 and r.memberjoinnotify:
                s = r.memberjoinnotify.room.properties[1].value
                i = r.memberjoinnotify.room.members[0].userdata
            elif r.payloadtype == 1002 and r.memberquitnotify:
                s = r.memberquitnotify.room.properties[0].value
                i = r.memberquitnotify.room.members[0].userdata
            i = i.decode('utf-8')
            i = json.loads(i)
        return s, i

    def decode_msg(self, message):
        msgs = []
        memcountmsg, msgcontent = self.processMessagePack(message)
        if msgcontent.get('type') == 9:
            name = msgcontent['extends']['nickname']
            content = msgcontent['text']
            msg = {'name': name, 'content': content, 'msg_type': 'danmaku'}
            msgs.append(msg)
        return msgs
