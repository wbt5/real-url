# 快手代码来源及思路：https://github.com/py-wuhao/ks_barrage

import aiohttp
import random
import time
import json
import re


class KuaiShou:
    heartbeat = b'\x08\x01\x1A\x07\x08'  # 发送心跳可固定
    heartbeatInterval = 20

    @staticmethod
    async def get_ws_info(url):
        """获取wss连接信息
        Args:
            直播间完整地址
        Returns:
            webSocketUrls:wss地址
            reg_datas:第一次send数据
            liveStreamId:
            token:
            page_id:
            :param url:
        """
        rid = url.split('/')[-1]
        url = 'https://m.gifshow.com/fw/live/' + str(rid)  # 移动版直播间地址
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, '
                          'like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'Cookie': 'did=web_e8436e86a8ec476c801c1d534f56db0c'}  # 请求失败则更换cookie中的did字段
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                wsFeedInfo = re.findall(r'wsFeedInfo":(.*),"liveExist', await resp.text())
                wsFeedInfo = json.loads(wsFeedInfo[0])
                liveStreamId = wsFeedInfo['liveStreamId']
                token = wsFeedInfo['token']
                webSocketUrls = wsFeedInfo['webSocketUrls'][0]

                reg_datas = []
                part1 = b'\x08\xC8\x01\x1A\xC8\x01\x0A\x98\x01'
                part2 = token.encode()
                part3 = b'\x12\x0B'
                part4 = liveStreamId.encode()
                part5 = b'\x3A\x1E'
                page_id = KuaiShou.get_page_id()
                part6 = page_id.encode()
                s = part1 + part2 + part3 + part4 + part5 + part6
                reg_datas.append(s)

        return webSocketUrls, reg_datas

    @staticmethod
    def get_page_id():
        charset = "bjectSymhasOwnProp-0123456789ABCDEFGHIJKLMNQRTUVWXYZ_dfgiklquvxz"
        page_id = ''
        for _ in range(0, 16):
            page_id += random.choice(charset)
        page_id += "_"
        page_id += str(int(time.time() * 1000))
        return page_id

    @staticmethod
    def decode_msg(data):
        msgs = []
        msg = {}
        s = MessageDecode(data)
        c = s.decode()
        if c.get('payloadType', 0) == 310:  # SC_FEED_PUSH = 310 时有弹幕数据
            m = s.feed_decode(c['payload'])  # 弹幕解码方法
            if m.get('comment'):
                for user in m.get('comment'):
                    msg['name'] = user.get('user').get('userName').encode('utf-16', 'surrogatepass').decode('utf-16')
                    msg['content'] = user.get('content').encode('utf-16', 'surrogatepass').decode('utf-16')
                    msg['msg_type'] = 'danmaku'
                    msgs.append(msg.copy())
                return msgs
            else:
                msg = {'name': '', 'content': '', 'msg_type': 'other'}
        else:
            msg = {'name': '', 'content': '', 'msg_type': 'other'}
        msgs.append(msg)
        return msgs


class MessageDecode:
    """
    返回的数据流解码
    """

    def __init__(self, buf):
        self.buf = buf
        self.pos = 0
        self.message = {}

    def __len__(self):
        return len(self.buf)

    def int_(self):
        res = 0
        i = 0
        while self.buf[self.pos] >= 128:
            res = res | (127 & self.buf[self.pos]) << 7 * i
            self.pos += 1
            i += 1
        res = res | self.buf[self.pos] << 7 * i
        self.pos += 1
        return res

    def decode(self):
        """
        服务器返回数据第一次解码
        Return:m
            payloadType:
            101: "SC_HEARTBEAT_ACK",
            103: "SC_ERROR",
            105: "SC_INFO",
            300: "SC_ENTER_ROOM_ACK",
            310: "SC_FEED_PUSH", # 310是弹幕信息
            330: "SC_RED_PACK_FEED",
            340: "SC_LIVE_WATCHING_LIST",
            370: "SC_GUESS_OPENED",
            371: "SC_GUESS_CLOSED",
            412: "SC_RIDE_CHANGED",
            441: "SC_BET_CHANGED",
            442: "SC_BET_CLOSED",
            645: "SC_LIVE_SPECIAL_ACCOUNT_CONFIG_STATE"
        """
        m = {}
        self.pos = 0
        length = len(self)
        while self.pos < length:
            t = self.int_()
            tt = t >> 3
            if tt == 1:
                m['payloadType'] = self.int_()
            elif tt == 2:
                m['compressionType'] = self.int_()
            elif tt == 3:
                m['payload'] = self.bytes()
            else:
                self.skipType(t & 7)
        return m

    def skipType(self, e):
        if e == 0:
            self.skip()
        elif e == 1:
            self.skip(8)
        elif e == 2:
            self.skip(self.int_())
        elif e == 3:
            while True:
                e = 7 & self.int_()
                if 4 != e:
                    self.skipType(e)
        elif e == 5:
            self.skip(4)
        else:
            raise Exception('跳过类型错误')

    def bytes(self):
        e = self.int_()
        if e + self.pos > len(self.buf):
            raise Exception('index out of range')
        res = self.buf[self.pos: (e + self.pos)]
        self.pos += e
        return res

    def skip(self, e=None):
        """跳过多少字节"""
        if e is None:
            while self.pos < len(self.buf):
                if 128 & self.buf[self.pos] == 0:
                    self.pos += 1
                    return
                self.pos += 1
            return
        self.pos += e
        if self.pos >= len(self.buf):
            self.pos -= 1

    def feed_decode(self, payload):
        """
        payload解码,即还原JS中的function SCWebFeedPush$decode(r, l)
        Args:
            decode函数返回的paylod
        Returns:
            m解码后的数据
        """
        self.pos = 0
        self.buf = payload
        m = {}
        length = len(self.buf)
        while self.pos < length:
            t = self.int_()
            tt = t >> 3
            if tt == 1:
                m['displayWatchingCount'] = self.string()
            elif tt == 2:
                m['displayLikeCount'] = self.string()
            elif tt == 3:
                m['pendingLikeCount'] = self.int_()
            elif tt == 4:
                m['pushInterval'] = self.int_()
            elif tt == 5:
                if not m.get('comment'):
                    m['comment'] = []
                m['comment'].append(self.comment_decode(self.buf, self.int_()))
            elif tt == 6:
                m['commentCursor'] = self.string()
            elif tt == 7:
                if not m.get('comboComment'):
                    m['comboComment'] = []
                m['comboComment'].append(self.comboComment_decode(self.buf, self.int_()))
            elif tt == 8:
                if not m.get('like'):
                    m['like'] = []
                m['like'].append(self.web_like_feed_decode(self.buf, self.int_()))
            elif tt == 9:  # 礼物
                if not m.get('gift'):
                    m['gift'] = []
                m['gift'].append(self.gift_decode(self.buf, self.int_()))
            elif tt == 10:
                m['giftCursor'] = self.string()
            elif tt == 11:
                if not m.get('systemNotice'):
                    m['systemNotice'] = []
                m['systemNotice'].append(self.systemNotice_decode(self.buf, self.int_()))
            elif tt == 12:
                if not m.get('share'):
                    m['share'] = []
                m['share'].append(self.share_decode(self.buf, self.int_()))
            else:
                self.skipType(t & 7)
        return m

    def comment_decode(self, r, l):
        c = self.pos + l
        m = {}
        while self.pos < c:
            t = self.int_()
            tt = t >> 3
            if tt == 1:
                m['id'] = self.string()
            elif tt == 2:
                m['user'] = self.user_info_decode(self.buf, self.int_())
            elif tt == 3:
                m['content'] = self.string()
            elif tt == 4:
                m['deviceHash'] = self.string()
            elif tt == 5:
                m['sortRank'] = self.int_()
            elif tt == 6:
                m['color'] = self.string()
            elif tt == 7:
                m['showType'] = self.int_()
            else:
                self.skipType(t & 7)
        return m

    def comboComment_decode(self, r, l):
        pass

    def systemNotice_decode(self, r, l):
        pass

    def share_decode(self, r, l):
        pass

    def user_info_decode(self, r, l):
        c = self.pos + l
        m = {}
        while self.pos < c:
            t = self.int_()
            tt = t >> 3
            if tt == 1:
                m['principalId'] = self.string()
            elif tt == 2:
                m['userName'] = self.string()
            elif tt == 3:
                m['headUrl'] = self.string()
            else:
                self.skipType(t & 7)
        return m

    def web_like_feed_decode(self, r, l):
        c = self.pos + l
        m = {}
        while self.pos < c:
            t = self.int_()
            tt = t >> 3
            if tt == 1:
                m['id'] = self.string()
            elif tt == 2:
                m['user'] = self.user_info_decode(self.buf, self.int_())
            elif tt == 3:
                m['sortRank'] = self.int_()
            elif tt == 4:
                m['deviceHash'] = self.string()
            else:
                self.skipType(t & 7)
        return m

    def gift_decode(self, r, l):
        c = self.pos + l
        m = {}
        while self.pos < c:
            t = self.int_()
            tt = t >> 3
            if tt == 1:
                m['id'] = self.string()
            elif tt == 2:
                m['user'] = self.user_info_decode(self.buf, self.int_())
            elif tt == 3:
                m['time'] = self.int_()
            elif tt == 4:
                m['giftId'] = self.int_()
            elif tt == 5:
                m['sortRank'] = self.int_()
            elif tt == 6:
                m['mergeKey'] = self.string()
            elif tt == 7:
                m['batchSize'] = self.int_()
            elif tt == 8:
                m['comboCount'] = self.int_()
            elif tt == 9:
                m['rank'] = self.int_()
            elif tt == 10:
                m['expireDuration'] = self.int_()
            elif tt == 11:
                m['clientTimestamp'] = self.int_()
            elif tt == 12:
                m['slotDisplayDuration'] = self.int_()
            elif tt == 13:
                m['starLevel'] = self.int_()
            elif tt == 14:
                m['styleType'] = self.int_()
            elif tt == 15:
                m['liveAssistantType'] = self.int_()
            elif tt == 16:
                m['deviceHash'] = self.string()
            elif tt == 17:
                m['danmakuDisplay'] = self.int_()
            else:
                self.skipType(t & 7)
        return m

    def string(self):
        e = self.bytes()
        n = len(e)
        if n < 1:
            return ""
        s = []
        t = 0
        while t < n:
            r = e[t]
            t += 1
            if r < 128:
                s.append(r)
            elif 191 < r < 224:
                s.append((31 & r) << 6 | 63 & e[t])
                t += 1
            elif 239 < r < 365:
                x = (7 & r) << 18 | (63 & e[t]) << 12
                t += 1
                y = (63 & e[t]) << 6
                t += 1
                z = 63 & e[t]
                t += 1
                r = (x | y | z) - 65536
                s.append(55296 + (r >> 10))
                s.append(56320 + (1023 & r))
            else:
                x = (15 & r) << 12
                y = (63 & e[t]) << 6
                t += 1
                z = 63 & e[t]
                t += 1
                s.append(x | y | z)
        string = ''
        for w in s:
            string += chr(w)
        return string
