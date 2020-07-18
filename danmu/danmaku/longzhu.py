import json
import aiohttp
import re


class LongZhu:
    heartbeat = None

    @staticmethod
    async def get_ws_info(url):
        rid = url.split('/')[-1]
        async with aiohttp.ClientSession() as session:
            async with session.get('http://m.longzhu.com/' + rid) as resp:
                res1 = await resp.text()
                roomid = re.search(r'var roomId = (\d+);', res1).group(1)
            async with session.get('http://idc-gw.longzhu.com/mbidc?roomId=' + roomid) as resp2:
                res2 = json.loads(await resp2.text())
                ws_url = res2['data']['redirect_to'] + '?room_id=' + roomid
        return ws_url, None

    @staticmethod
    def decode_msg(message):
        msgs = []
        msg = {'name': '', 'content': '', 'msg_type': 'other'}
        message = json.loads(message)
        type_ = message['type']
        # type_ == 'gift' 礼物
        if type_ == 'chat':
            msg['name'] = message['msg']['user']['username']
            msg['content'] = (message['msg']['content']).strip()
            msg['msg_type'] = 'danmaku'
        elif type_ == 'commonjoin':
            msg['name'] = message['msg']['user']['username']
            msg['content'] = message['msg']['userMessage']
            msg['msg_type'] = 'danmaku'
        msgs.append(msg.copy())
        return msgs
