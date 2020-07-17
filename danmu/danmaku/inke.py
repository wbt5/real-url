import aiohttp
import re
import time
import json


class Inke:
    heartbeat = None

    @staticmethod
    async def get_ws_info(url):
        uid = re.search(r'uid=(\d+)', url).group(1)
        roomid = id = re.search(r'&id=(\d+)', url).group(1)
        t = int(time.time() * 1e3)
        cr = 'https://chatroom.inke.cn/url?roomid={}&uid={}&id={}&access_from=pc_web&_t={}'.format(roomid, uid, id, t)
        async with aiohttp.ClientSession() as session:
            async with session.get(cr) as resp:
                res = await resp.text()
                wss_url = json.loads(res).get('url')
        return wss_url, None

    @staticmethod
    def decode_msg(data):
        msgs = []
        name = content = ''
        msg_type = 'other'
        message = json.loads(data)
        ms = message['ms']
        c = ms[-1].get('c', 0)
        if c:
            tp = ms[-1].get('tp', 0)
            if tp == 'pub' or tp == 'color':
                name = ms[0].get('from').get('nic', '')
            elif tp == 'user_join_tip':
                name = ms[0].get('u').get('nic', '')
            else:
                name = 'sys'
            content = c
            msg_type = 'danmaku'
        msg = {'name': name, 'content': content, 'msg_type': msg_type}
        msgs.append(msg)
        return msgs
