from . import kuaishou_pb2 as pb
import aiohttp
import re
import json
import time
import random


class KuaiShou:
    heartbeatInterval = 20

    @staticmethod
    async def get_ws_info(url):
        """获取wss连接信息
        Args:
            直播间完整地址
        Returns:
            webSocketUrls:wss地址
            data:第一次send数据
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
            'Cookie': 'did=web_d563dca728d28b00336877723e0359ed'}  # 请求失败则更换cookie中的did字段
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                res = await resp.text()

        wsfeedinfo = re.search(r'wsFeedInfo":(.*),"liveExist', res)
        if wsfeedinfo:
            wsfeedinfo = json.loads(wsfeedinfo.group(1))
        else:
            raise Exception('找不到 wsFeedInfo，可能链接错误或 Cookie 过期')

        livestreamid, [websocketurls], token = wsfeedinfo.values()
        page_id = KuaiShou.get_page_id()

        p, s = pb.SocketMessage(), pb.CSWebEnterRoom()
        s.liveStreamId, s.pageId, s.token = livestreamid, page_id, token
        p.payload = s.SerializeToString()
        p.payloadType = 200
        reg_data = p.SerializeToString()

        t = pb.CSWebHeartbeat()
        t.timestamp = int(time.time() * 1000)
        p.payload = t.SerializeToString()
        p.payloadType = 1
        KuaiShou.heartbeat = p.SerializeToString()  # 心跳可固定

        return websocketurls, [reg_data]

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
    def decode_msg(message):
        msgs = [{'name': '', 'content': '', 'msg_type': 'other'}]

        p, s = pb.SocketMessage(), pb.SCWebFeedPush()
        p.ParseFromString(message)
        if p.payloadType == 310:
            s.ParseFromString(p.payload)

            def f(*feeds):
                gift = {
                    1: '荧光棒', 2: '棒棒糖', 3: '荧光棒', 4: 'PCL加油', 7: '么么哒', 9: '啤酒', 10: '甜甜圈',
                    14: '钻戒', 16: '皇冠', 25: '凤冠', 33: '烟花', 41: '跑车', 56: '稳', 113: '火箭',
                    114: '玫瑰', 132: '绷带', 133: '平底锅', 135: '红爸爸', 136: '蓝爸爸', 137: '铭文碎片',
                    143: '太阳女神', 147: '赞', 149: '血瓶', 150: 'carry全场', 152: '大红灯笼', 156: '穿云箭',
                    159: '膨胀了', 160: '秀你一脸', 161: 'MVP', 163: '加油', 164: '猫粮', 165: '小可爱',
                    169: '男神', 172: '联盟金猪', 173: '有钱花', 193: '蛋糕', 197: '棒棒糖', 198: '瓜',
                    199: '小可爱', 201: '赞', 207: '快手卡', 208: '灵狐姐', 216: 'LPL加油', 218: '烟花',
                    219: '告白气球', 220: '大红灯笼', 221: '怦然心动', 222: '凤冠', 223: '火箭', 224: '跑车',
                    225: '穿云箭', 226: '金话筒', 227: 'IG冲鸭', 228: 'GRF冲鸭', 229: 'FPX冲鸭', 230: 'FNC冲鸭',
                    231: 'SKT冲鸭', 232: 'SPY冲鸭', 233: 'DWG冲鸭', 234: 'G2冲鸭', 235: '爆单', 236: '入团券',
                    237: '陪着你540', 238: '支持牌', 239: '陪着你', 242: '金龙', 243: '豪车幻影', 244: '超级6',
                    245: '水晶', 246: '金莲', 247: '福袋', 248: '铃铛', 249: '巧克力', 250: '感恩的心',
                    254: '武汉加油', 256: '金龙', 257: '财神', 258: '金龙', 259: '天鹅湖', 260: '珍珠',
                    261: '金莲', 262: '招财猫', 263: '铃铛', 264: '巧克力', 266: '幸运魔盒', 267: '吻你',
                    268: '梦幻城堡', 269: '游乐园', 271: '萌宠', 272: '小雪豹', 275: '喜欢你', 276: '三级头',
                    277: '喜欢你', 278: '财神', 279: '锦鲤', 281: '廉颇', 282: '开黑卡', 283: '付费直播门票（不下线）',
                    285: '喜欢你呀', 286: '629', 287: '真爱大炮', 289: '玫瑰花园', 290: '珠峰', 292: '鹿角',
                    296: '666', 297: '超跑车队', 298: '奥利给', 302: '互粉', 303: '冰棒', 304: '龙之谷',
                    306: '浪漫游轮', 307: '壁咚', 308: '壁咚', 309: '鹿角', 310: '么么哒', 311: '私人飞机',
                    312: '巅峰票', 313: '巅峰王者', 315: '莫吉托', 316: '地表最强', 318: '阳光海滩', 319: '12号唱片'
                }
                infos = [{'name': '', 'content': '', 'msg_type': 'other'}]
                for feed in feeds:
                    if feed:
                        for i in feed:
                            name = i.user.userName
                            content = i.content if hasattr(i, 'content') else '送 ' + gift.get(i.giftId, '') \
                                if hasattr(i, 'giftId') else '点亮了 ❤'
                            info = {'name': name, 'content': content, 'msg_type': 'danmaku'}
                            infos.append(info.copy())
                return infos

            msgs = f(s.commentFeeds, s.giftFeeds, s.likeFeeds)

        return msgs
