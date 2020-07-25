import aiohttp
import asyncio
import re

from .bilibili import Bilibili
from .douyu import Douyu
from .huya import Huya
from .kuaishou import KuaiShou
from .huomao import HuoMao
from .egame import eGame
from .huajiao import HuaJiao
from .inke import Inke
from .cc import CC
from .kugou import KuGou
from .zhanqi import ZhanQi
from .longzhu import LongZhu
from .pps import QiXiu
from .qf import QF
from .laifeng import LaiFeng
from .look import Look

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
                     'look.163.com': Look}.items():
            if re.match(r'^(?:http[s]?://)?.*?%s/(.+?)$' % u, url):
                self.__site = s
                self.__u = u
                break
        if self.__site is None:
            print('Invalid link!')
            exit
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
        await self.heartbeats()

    async def start(self):
        if self.__u == 'huajiao.com':
            await self.init_ws_huajiao()
        else:
            await self.init_ws()
            await asyncio.gather(
                self.heartbeats(),
                self.fetch_danmaku(),
            )
