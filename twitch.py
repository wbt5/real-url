# -*- coding: utf-8 -*-
# @Time: 2021/5/2 16:20
# @Project: real-url
# @Author: wbt5
# @Blog: https://wbt5.com

import json
import re
from urllib.parse import urlencode

# twitch 直播需要科学上网
import requests


class Twitch:

    def __init__(self, rid):
        # rid = channel_name
        self.rid = rid
        with requests.Session() as self.s:
            pass

    def get_client_id(self):
        try:
            res = self.s.get(f'https://www.twitch.tv/{self.rid}').text
            client_id = re.search(r'"Client-ID":"(.*?)"', res).group(1)
            return client_id
        except requests.exceptions.ConnectionError:
            raise Exception('ConnectionError')

    def get_sig_token(self):
        data = {
            "operationName": "PlaybackAccessToken_Template",
            "query": "query PlaybackAccessToken_Template($login: String!, $isLive: Boolean!, $vodID: ID!, "
                     "$isVod: Boolean!, $playerType: String!) {  streamPlaybackAccessToken(channelName: $login, "
                     "params: {platform: \"web\", playerBackend: \"mediaplayer\", playerType: $playerType}) @include("
                     "if: $isLive) {    value    signature    __typename  }  videoPlaybackAccessToken(id: $vodID, "
                     "params: {platform: \"web\", playerBackend: \"mediaplayer\", playerType: $playerType}) @include("
                     "if: $isVod) {    value    signature    __typename  }}",
            "variables": {
                "isLive": True,
                "login": self.rid,
                "isVod": False,
                "vodID": "",
                "playerType": "site"
            }
        }

        headers = {
            'Client-ID': self.get_client_id(),
            'Referer': 'https://www.twitch.tv/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/90.0.4430.93 Safari/537.36',
        }
        res = self.s.post('https://gql.twitch.tv/gql', headers=headers, data=json.dumps(data)).json()
        try:
            token, signature, _ = res['data']['streamPlaybackAccessToken'].values()
        except AttributeError:
            raise Exception("Channel does not exist")

        return signature, token

    def get_real_url(self):
        signature, token = self.get_sig_token()
        params = {
            'allow_source': 'true',
            'dt': 2,
            'fast_bread': 'true',
            'player_backend': 'mediaplayer',
            'playlist_include_framerate': 'true',
            'reassignments_supported': 'true',
            'sig': signature,
            'supported_codecs': 'vp09,avc1',
            'token': token,
            'cdm': 'wv',
            'player_version': '1.4.0',
        }
        url = f'https://usher.ttvnw.net/api/channel/hls/{self.rid}.m3u8?{urlencode(params)}'
        return url


def get_real_url(rid):
    try:
        tw = Twitch(rid)
        return tw.get_real_url()
    except Exception as e:
        print('Exception：', e)
        return False


if __name__ == '__main__':
    r = input('请输入 twitch 房间名：\n')
    print(get_real_url(r))
