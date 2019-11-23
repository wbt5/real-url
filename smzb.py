# 收米直播（http://smzb.tv:66/live/）所有直播间。


import requests
import re
import json


def get_all_rooms():
    room_url = 'http://api.shoumilive.com:83/pc/anchor.json'
    try:
        response = requests.get(url=room_url).text
        response_json = json.loads(re.findall(r'anchor\(([\s\S]*)\)', response)[0])
        all_hot = response_json.get('data').get('hot')
        all_rooms = dict()
        for room in all_hot:
            room_id  = room.get('room_num')
            room_title = str(room_id) + ':' + room.get('title')
            room_flv = get_real_url(str(room_id))
            all_rooms[room_title] = room_flv
    except:
        all_rooms = '获取错误'
    return all_rooms



def get_real_url(rid):
    room_url = 'http://api.shoumilive.com:83/pc/room/{}.json'.format(rid)
    try:
        response = requests.get(url=room_url).text
        response_json = json.loads(re.findall(r'livePath\(([\s\S]*)\)', response)[0])
        real_url = response_json.get('data').get('flv_hd')
    except:
        real_url = '获取错误'
    return real_url


if __name__ == "__main__":
    print(get_all_rooms())
