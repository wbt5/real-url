# AcFun直播现在属于快手旗下了，其JS源码中也可以看到很多名为'kuaishou'的变量，所以和快手直播弹幕的获取方法有点类似，都使用了protobuf压缩数据。
# 在mplayer-live.xxx.js中可以看到所有websocket过程。奇怪的是，其序列化和反序列化时代码并不统一，可能有啥"特殊意义"我没看懂。
# ws请求过程：Register--EnterRoom--Heartbeat,其中Register后返回的第一条数据里有sessionkey和instanceid。
# 在Chrome调试时发现客户端一直会向服务器发送：每1秒一次ping；每10秒一次keepalive，模拟实现时，不发送也正常。
import base64
import gzip
import struct
import time

import requests
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from . import acfun_pb2 as pb


class AcFun:
    ws_url = 'wss://link.xiatou.com/'

    def __init__(self, rid):
        self.encryptionmode = 0  # 加密模式，0不加密，1时key=ssecurity，2时key=sessionkey
        self.seqId = 0  # 客户端发送请求时都会加1
        self.payload_len = 0
        self.sessionkey = b''
        self.instanceid = 0  # 初始值0
        self.gift = {  # 有些直播间的礼物编号不一样，实际打开直播间页面会有一次XHR请求
            1: '香蕉',
            17: '快乐水',
            9: '告白',
            35: '氧气瓶',
            4: '牛啤',
            33: '情书',
            8: '星蕉雨',
            31: '金坷垃',
            34: '狗粮',
            2: '吃瓜',
            12: '打Call',
            32: '变身腰带',
            15: 'AC机娘',
            16: '猴岛',
            10: '666',
            11: '菜鸡',
            30: '鸽鸽',
            13: '立FLAG',
            6: '魔法棒',
            7: '好人卡',
            14: '窜天猴',
            21: '生日快乐',
            5: '手柄',
            29: '大触'
        }
        # 下面获取一些加入房间所需注册参数
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': '_did=H5_',
            'referer': 'https://m.acfun.cn/'
        }
        url = 'https://id.app.acfun.cn/rest/app/visitor/login'
        form_data = 'sid=acfun.api.visitor'
        with requests.Session() as s:
            res = s.post(url, data=form_data, headers=headers).json()
        status, *d = res.values()
        if status == 0:
            # 未登陆访客获取的3个参数
            acsecurity, self.uid, visitor_st = d
            self.ssecurity = base64.b64decode(acsecurity)
            self.token = visitor_st.encode()
        else:
            raise Exception('token 获取错误')
        url = 'https://api.kuaishouzt.com/rest/zt/live/web/startPlay'
        params = {
            'subBiz': 'mainApp',
            'kpn': 'ACFUN_APP',
            'kpf': 'OUTSIDE_IOS_H5',
            'userId': self.uid,
            'did': 'H5_',
            'acfun.api.visitor_st': visitor_st
        }
        data = 'authorId={}&pullStreamType=SINGLE_HLS'.format(rid)
        res = s.post(url, params=params, data=data, headers=headers).json()
        if res['result'] == 1:
            data = res['data']
            # 获取直播间的几个参数
            self.availabletickets, *_ = data['availableTickets']
            self.enterroomattach = data['enterRoomAttach']
            self.liveid = data['liveId']
        else:
            raise Exception('直播已关闭')

    @staticmethod
    # aes加密，iv随机；key值取决去encryptionmode
    def aes_encode(t, key):
        t = pad(t, AES.block_size)
        iv = Random.new().read(AES.block_size)
        mode = AES.MODE_CBC
        c = AES.new(key, mode, iv)
        res = c.encrypt(t)
        return iv + res  # 把iv加到头部

    @staticmethod
    # 这里传入的待解密数据不用补全，一直都是16的整数倍。key值取决去encryptionmode。pkcs7模式去掉最后的填充padding。
    def aes_decode(t, key):
        iv = t[:16]
        n = t[16:]
        # n = pad(n, AES.block_size)
        mode = AES.MODE_CBC
        c = AES.new(key, mode, iv)
        res = c.decrypt(n)
        length = len(res)
        padding = res[length - 1]
        res = res[0:length - padding]
        return res

    def register(self):
        # 注册
        p = pb.RegisterRequest()
        p.appActiveStatus = 1
        p.appInfo.appName = 'link-sdk'
        p.appInfo.sdkVersion = '1.2.1'
        p.deviceInfo.deviceModel = 'h5'
        p.deviceInfo.platformType = 6
        p.instanceId = 0
        p.presenceStatus = 1
        p.ztCommonInfo.kpn = 'ACFUN_APP'
        p.ztCommonInfo.kpf = 'OUTSIDE_IOS_H5'
        p.ztCommonInfo.uid = self.uid
        register_data = p.SerializeToString()
        self.encryptionmode = 1
        self.seqId = 1
        return register_data

    def keepalive(self):
        # keepalive
        p = pb.KeepAliveRequest()
        p.appActiveStatus = 1
        p.presenceStatus = 1
        keepalive_data = p.SerializeToString()
        self.encryptionmode = 2
        self.seqId += 1
        return keepalive_data

    def ping(self):
        # ping
        p = pb.PingRequest()
        # p.pingType = 2
        ping_data = p.SerializeToString()
        self.seqId += 1
        self.encryptionmode = 2
        return ping_data

    def ztlivecsenterroom(self):
        return self.cscmd('ZtLiveCsEnterRoom')

    def ztlivecsheartbeat(self):
        # 心跳数据
        return self.cscmd('ZtLiveCsHeartbeat')

    def cscmd(self, payload_type):
        p = getattr(pb, payload_type)()

        if payload_type == 'ZtLiveCsEnterRoom':
            p.isAuthor = False
            p.reconnectCount = 0
            p.enterRoomAttach = self.enterroomattach
            p.clientLiveSdkVersion = 'kwai-acfun-live-link'
        elif payload_type == 'ZtLiveCsHeartbeat':
            p.sequence = self.seqId
            p.clientTimestampMs = int(time.time() * 1000)

        payload = p.SerializeToString()
        p = pb.CsCmd()
        p.cmdType = payload_type
        p.ticket = self.availabletickets
        p.payload = payload
        p.liveId = self.liveid
        cscmd_data = p.SerializeToString()

        self.seqId += 1
        self.encryptionmode = 2
        return cscmd_data

    def encode_payload(self, payload_type):
        # 要发送的原始数据都是先序列化再拼接
        c = {
            'keepalive': 'Basic.KeepAlive',
            'register': 'Basic.Register',
            'ping': 'Basic.Ping',
            'ztlivecsenterroom': 'Global.ZtLiveInteractive.CsCmd',
            'ztlivecsheartbeat': 'Global.ZtLiveInteractive.CsCmd'
        }
        p = pb.UpstreamPayload()
        p.command = c[payload_type]
        p.retryCount = 1
        p.payloadData = getattr(self, payload_type)()
        p.seqId = self.seqId
        p.subBiz = 'mainApp'
        e = p.SerializeToString()
        key = self.ssecurity if self.encryptionmode == 1 else self.sessionkey
        payload_data = AcFun.aes_encode(e, key) if self.encryptionmode != 0 else e
        self.payload_len = len(e)
        return payload_data

    def encode_head(self):
        # 头部数据,里面有原始数据长度
        p = pb.PacketHeader()
        p.appId = 13
        p.decodedPayloadLen = self.payload_len
        p.encryptionMode = self.encryptionmode
        p.instanceId = self.instanceid
        p.kpn = 'ACFUN_APP'
        p.seqId = self.seqId
        if self.encryptionmode == 1:
            p.tokenInfo.tokenType = 1
            p.tokenInfo.token = self.token
        p.uid = self.uid
        head = p.SerializeToString()
        return head

    def encode_packet(self, payload_type):
        # 数据组成:固定数据 + 头部长度 + 原始数据长度 + 头部 + 原始数据
        body = self.encode_payload(payload_type)
        head = self.encode_head()
        data = struct.pack('!HHII', 43981, 1, len(head), len(body))
        data += head + body
        return data

    def decode_packet(self, data):
        # 数据解包
        msgs = [{'name': '', 'content': '', 'msg_type': 'other'}]

        head_length, body_length = struct.unpack('!II', data[4:12])

        if 12 + head_length + body_length != len(data):
            raise Exception('downstream message size is not correct')

        # 头部解包
        e = data[12:head_length + 12]
        c = pb.PacketHeader()
        c.ParseFromString(e)
        encryptionmode = c.encryptionMode  # 根据加密模式确定解密的key

        # body解包
        h = data[head_length + 12:]
        key = self.ssecurity if encryptionmode == 1 else self.sessionkey
        n = AcFun.aes_decode(h, key) if encryptionmode != 0 else h
        u = pb.DownstreamPayload()
        u.ParseFromString(n)

        # header = c
        # body = u
        payload = u.payloadData
        command = u.command  # 根据command确定返回数据类型
        # print(command)

        if command == 'Basic.Register':
            # websocket第一次返回数据,确定sessKey和instanceId
            p = pb.RegisterResponse()
            p.ParseFromString(payload)
            self.sessionkey = p.sessKey
            self.instanceid = p.instanceId

        elif command == 'Push.ZtLiveInteractive.Message':  # 'Push.ZtLiveInteractive.Message'
            a = pb.ZtLiveScMessage()
            a.ParseFromString(payload)
            o = a.messageType
            s = a.payload

            if a.compressionType == 2:
                s = gzip.decompress(s)

            if o == 'ZtLiveScTicketInvalid':
                raise Exception('ZtLiveScTicketInvalid')

            # o可为'ZtLiveScNotifySignal' 'ZtLiveScActionSignal' 等,弹幕礼物入场点赞等在ZtLiveScActionSignal中
            elif o == 'ZtLiveScActionSignal':
                p = getattr(pb, o)()
                p.ParseFromString(s)

                for i in p.item:
                    p = getattr(pb, i.signalType)()
                    # signalType:
                    # CommonActionSignalComment 评论
                    # CommonActionSignalGift 礼物
                    # CommonActionSignalUserEnterRoom 入场
                    # CommonActionSignalLike 点赞
                    # CommonActionSignalUserFollowAuthor 关注主播
                    # 等等等
                    u = {
                        'CommonActionSignalUserEnterRoom': '进入直播间',
                        'CommonActionSignalUserFollowAuthor': '关注了主播',
                        'CommonActionSignalComment': '',
                        'CommonActionSignalLike': '点赞了❤',
                        'CommonActionSignalGift': ''
                    }

                    for a_payload in i.payload:  # i.payload 是 repeated 类型
                        p.ParseFromString(a_payload)

                        if i.signalType in u.keys():
                            user = p.userInfo.nickname
                            content = u[i.signalType]
                            if i.signalType == 'CommonActionSignalComment':
                                content = p.content
                            elif i.signalType == 'CommonActionSignalGift':
                                content = '送出 ' + self.gift.get(p.giftId, '')

                            msg = {'name': user, 'content': content, 'msg_type': 'danmaku'}
                            msgs.append(msg.copy())
        return msgs
