# 部分弹幕功能代码来自项目：https://github.com/IsoaSFlus/danmaku，感谢大佬
# 快手弹幕代码来源及思路：https://github.com/py-wuhao/ks_barrage，感谢大佬
# 仅抓取用户弹幕，不包括入场提醒、礼物赠送等。

import asyncio
import danmaku


async def printer(q):
    while True:
        m = await q.get()
        if m['msg_type'] == 'danmaku':
            print(f'{m["name"]}：{m["content"]}')


async def main(url):
    q = asyncio.Queue()
    dmc = danmaku.DanmakuClient(url, q)
    asyncio.create_task(printer(q))
    await dmc.start()


a = input('请输入直播间地址：\n')
asyncio.run(main(a))

# 虎牙：https://www.huya.com/11352915
# 斗鱼：https://www.douyu.com/85894
# B站：https://live.bilibili.com/70155
# 快手：https://live.kuaishou.com/u/jjworld126
# 火猫：
# 企鹅电竞：https://egame.qq.com/383204988
