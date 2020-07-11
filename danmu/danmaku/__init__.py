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
                     'cc.163.com': CC}.items():
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
        for reg_data in reg_datas:
            await self.__ws.send_bytes(reg_data)

    async def heartbeats(self):
        while not self.__stop:
            await asyncio.sleep(self.__site.heartbeatInterval)
            try:
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
        
    async def init_ws_inke(self):
        ws_url = await self.__site.get_ws_info(self.__url)
        self.__ws = await self.__hs.ws_connect(ws_url)
        await self.fetch_danmaku()

    async def start(self):
        if self.__u == 'huajiao.com':
            await self.init_ws_huajiao()
        elif self.__u == 'inke.cn':
            await self.init_ws_inke()
        else:
            await self.init_ws()
            await asyncio.gather(
                self.heartbeats(),
                self.fetch_danmaku(),
            )
