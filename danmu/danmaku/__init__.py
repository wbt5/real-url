import asyncio
import re

import aiohttp

from ._173 import YiQiShan
from .acfun import AcFun
from .bilibili import Bilibili
from .cc import CC
from .douyu import Douyu
from .egame import eGame
from .huajiao import HuaJiao
from .huomao import HuoMao
from .huya import Huya
from .inke import Inke
from .kuaishou import KuaiShou
from .kugou import KuGou
from .laifeng import LaiFeng
from .longzhu import LongZhu
from .look import Look
from .pps import QiXiu
from .qf import QF
from .zhanqi import ZhanQi

__all__ = ['DanmakuClient']


class DanmakuClient:
    def __init__(self, url, q):
        self.__url = ''
        self.__site = None
        self.__hs = None
        self.__ws = None
        self.__stop = False
        self.__dm_queue = q
        self.__link_status = True
        if 'http://' == url[:7] or 'https://' == url[:8]:
            self.__url = url
        else:
            self.__url = 'http://' + url
        for u, s in {'douyu.com': Douyu,
                     'live.bilibili.com': Bilibili,
                     'huya.com': Huya,
                     'huomao.com': HuoMao,
                     'kuaishou.com': KuaiShou,
                     'egame.qq.com': eGame,
                     'huajiao.com': HuaJiao,
                     'inke.cn': Inke,
                     'cc.163.com': CC,
                     'fanxing.kugou.com': KuGou,
                     'zhanqi.tv': ZhanQi,
                     'longzhu.com': LongZhu,
                     'pps.tv': QiXiu,
                     'qf.56.com': QF,
                     'laifeng.com': LaiFeng,
                     'look.163.com': Look,
                     'acfun.cn': AcFun,
                     '173.com': YiQiShan}.items():
            if re.match(r'^(?:http[s]?://)?.*?%s/(.+?)$' % u, url):
                self.__site = s
                self.__u = u
                break
        if self.__site is None:
            print('Invalid link!')
            exit()
        self.__hs = aiohttp.ClientSession()

    async def init_ws(self):
        ws_url, reg_datas = await self.__site.get_ws_info(self.__url)
        self.__ws = await self.__hs.ws_connect(ws_url)
        if reg_datas:
            for reg_data in reg_datas:
                if self.__u == 'qf.56.com' or self.__u == 'laifeng.com' or self.__u == 'look.163.com':
                    await self.__ws.send_str(reg_data)
                else:
                    await self.__ws.send_bytes(reg_data)

    async def heartbeats(self):
        while not self.__stop and self.__site.heartbeat:
            await asyncio.sleep(self.__site.heartbeatInterval)
            try:
                if self.__u == 'qf.56.com' or self.__u == 'laifeng.com' or self.__u == 'look.163.com':
                    await self.__ws.send_str(self.__site.heartbeat)
                else:
                    await self.__ws.send_bytes(self.__site.heartbeat)
            except:
                pass

    async def fetch_danmaku(self):
        while not self.__stop:
            async for msg in self.__ws:
                self.__link_status = True
                ms = self.__site.decode_msg(msg.data)
                for m in ms:
                    await self.__dm_queue.put(m)
            await asyncio.sleep(1)
            await self.init_ws()
            await asyncio.sleep(1)

    async def init_ws_huajiao(self):
        rid = re.search(r'\d+', self.__url).group(0)
        s = self.__site(rid)
        self.__ws = await self.__hs.ws_connect(self.__site.ws_url)
        await self.__ws.send_bytes(s.sendHandshakePack())
        count = 0
        async for msg in self.__ws:
            if count == 0:
                await self.__ws.send_bytes(s.sendLoginPack(msg.data))
            elif count == 1:
                await self.__ws.send_bytes(s.sendJoinChatroomPack(msg.data))
            elif count > 2:
                ms = s.decode_msg(msg.data)
                for m in ms:
                    await self.__dm_queue.put(m)
            count += 1

    async def init_ws_acfun(self, s):
        self.__ws = await self.__hs.ws_connect(self.__site.ws_url)
        await self.__ws.send_bytes(s.encode_packet('register'))

    async def ping_acfun(self, s):
        while True:
            await asyncio.sleep(1)
            await self.__ws.send_bytes(s.encode_packet('ping'))

    async def keepalive_acfun(self, s):
        while True:
            await asyncio.sleep(50)
            await self.__ws.send_bytes(s.encode_packet('keepalive'))

    async def heartbeat_acfun(self, s):
        while True:
            await asyncio.sleep(10)
            await self.__ws.send_bytes(s.encode_packet('ztlivecsheartbeat'))

    async def fetch_danmaku_acfun(self, s):
        count = 0
        async for msg in self.__ws:
            self.__link_status = True
            ms = s.decode_packet(msg.data)
            if count == 0:
                await self.__ws.send_bytes(s.encode_packet('ztlivecsenterroom'))
                count += 1
            for m in ms:
                await self.__dm_queue.put(m)

    async def init_ws_173(self, s):
        self.__ws = await self.__hs.ws_connect(self.__site.ws_url)
        await self.__ws.send_bytes(s.pack('startup'))
        await asyncio.sleep(1)
        await self.__ws.send_bytes(s.pack('enterroomreq'))

    async def tcphelloreq_173(self, s):
        while True:
            await asyncio.sleep(10)
            await self.__ws.send_bytes(s.pack('tcphelloreq'))

    async def roomhelloreq_173(self, s):
        while True:
            await asyncio.sleep(5)
            await self.__ws.send_bytes(s.pack('roomhelloreq'))

    async def fetch_danmaku_173(self, s):
        async for msg in self.__ws:
            self.__link_status = True
            ms = s.unpack(msg.data)
            for m in ms:
                await self.__dm_queue.put(m)

    async def start(self):
        if self.__u == 'huajiao.com':
            await self.init_ws_huajiao()
        elif self.__u == 'acfun.cn':
            rid = re.search(r'\d+', self.__url).group(0)
            s = self.__site(rid)
            await self.init_ws_acfun(s)
            await asyncio.gather(
                self.ping_acfun(s),
                self.fetch_danmaku_acfun(s),
                self.keepalive_acfun(s),
                self.heartbeat_acfun(s),
            )
        elif self.__u == '173.com':
            rid = self.__url.split('/')[-1]
            s = self.__site(rid)
            await self.init_ws_173(s)
            await asyncio.gather(
                self.fetch_danmaku_173(s),
                self.tcphelloreq_173(s),
                self.roomhelloreq_173(s),
            )
        else:
            await self.init_ws()
            await asyncio.gather(
                self.heartbeats(),
                self.fetch_danmaku(),
            )

    async def stop(self):
        self.__stop = True
        await self.__hs.close()
