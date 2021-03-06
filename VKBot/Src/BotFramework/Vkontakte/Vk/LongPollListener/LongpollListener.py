import json
import logging

import requests as requests

from Src.BotFramework.Vkontakte.Vk.Utils.VkApiCore import VkCore


class LongPollListener:
    def __init__(self, vk_api_core: VkCore):
        self.core = vk_api_core

    def _get_long_poll_server(self):
        return self.core.method('groups.getLongPollServer', {'group_id': '182157757'})

    def _get_long_poll_data(self):
        _r_data = self._get_long_poll_server()
        key = None
        server = None
        ts = None
        if _r_data is not None:  # if code was 200 OK
            _map = json.loads(_r_data)
            if 'response' in _map:
                _res = _map['response']
                if 'key' in _res and 'server' in _res and 'ts' in _res:
                    key = _res['key']
                    server = _res['server']
                    ts = _res['ts']
                else:
                    logging.critical("Cannot get one of needed params for server in request vk")
                    raise KeyError('Cannot get one of needed params for server in request vk')
            else:
                logging.critical("Something went wrong.. No 'response' key in str dict [Probably no str token]")
                raise ValueError('Something went wrong.. No \'response\' key in str dict [Probably no str token]')
        else:
            logging.critical("Bad response for vk api")
            raise IOError('Bad response for vk api')
        return key, ts, server

    @staticmethod
    def _get_long_poll_server_url(ts, key, server: str, wait=25) -> str:
        url = server.replace('\\', '')
        url += '?act=a_check&key={0}&ts={1}&wait={2}'.format(key, ts, wait)
        return url

    def listen(self):
        key, ts, server = self._get_long_poll_data()
        correct_url = self._get_long_poll_server_url(ts, key, server)
        while True:
            _w_res = requests.get(correct_url).json()

            if 'ts' in _w_res:
                ts = _w_res['ts']
            if 'updates' in _w_res:
                _update_list = _w_res['updates']
                for update in _update_list:
                    yield update
            correct_url = self._get_long_poll_server_url(ts, key, server)
