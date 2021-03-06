import requests
import requests_async


class TwitchCore:
    def __init__(self,client_id: str, oauth_token: str):
        self.client_id = client_id
        self.oauth_token = oauth_token
        self._V5_KRAKEN_URL = 'https://api.twitch.tv/kraken'
        self._NEW_HELIX_URL = 'https://api.twitch.tv/helix'

    # Kraken region

    def kraken_request(self, method_name: str, uri_args: dict = None, headers_new: dict = None,
                       method: str = 'get', json=None, files=None):
        if uri_args is not None:
            full_url = "{0}/{1}?{2}".format(self._V5_KRAKEN_URL,
                                            method_name,
                                            '&'.join("{0}={1}".format(key, uri_args[key]) for key in uri_args))
        else:
            full_url = "{0}/{1}".format(self._V5_KRAKEN_URL, method_name)

        headers = {"Client-ID": self.client_id,
                   "Authorization": "OAuth {0}".format(self.oauth_token),
                   "Accept": "application/vnd.twitchtv.v5+json"}

        if headers_new is not None:
            headers.update(headers_new)
        print(full_url)

        return self._make_request(url=full_url, method=method, headers=headers, json=json, files=files)

    async def kraken_request_async(self, method_name: str, uri_args: dict = None, headers_new: dict = None,
                                   method: str = 'get', json=None, files=None):
        if uri_args is not None:
            full_url = "{0}/{1}?{2}".format(self._V5_KRAKEN_URL,
                                            method_name,
                                            '&'.join("{0}={1}".format(key, uri_args[key]) for key in uri_args))
        else:
            full_url = "{0}/{1}".format(self._V5_KRAKEN_URL, method_name)

        headers = {"Client-ID": self.client_id,
                   "Authorization": "OAuth {0}".format(self.oauth_token),
                   "Accept": "application/vnd.twitchtv.v5+json"}

        if headers_new is not None:
            headers.update(headers_new)

        return await self._make_async_request(url=full_url, method=method, headers=headers, json=json, files=files)

    # Kraken region ends

    # Helix region

    def helix_request(self, method_name: str, uri_args: dict = None, headers_new: dict = None,
                      method: str = 'get', json=None, files=None):
        if uri_args is not None:
            full_url = "{0}/{1}?{2}".format(self._NEW_HELIX_URL,
                                            method_name,
                                            '&'.join("{0}={1}".format(key, uri_args[key]) for key in uri_args))
        else:
            full_url = "{0}/{1}".format(self._V5_KRAKEN_URL, method_name)

        headers = {"Client-ID": self.client_id, "authorization": "Bearer {0}".format(self.oauth_token)}

        if headers_new is not None:
            headers.update(headers_new)

        return self._make_request(url=full_url, method=method, headers=headers, json=json, files=files)

    async def helix_request_async(self, method_name: str, uri_args: dict = None, headers_new: dict = None,
                                  method: str = 'get', json=None, files=None):
        if uri_args is not None:
            full_url = "{0}/{1}?{2}".format(self._NEW_HELIX_URL,
                                            method_name,
                                            '&'.join("{0}={1}".format(key, uri_args[key]) for key in uri_args))
        else:
            full_url = "{0}/{1}".format(self._V5_KRAKEN_URL, method_name)

        headers = {"Client-ID": self.client_id, "authorization": "Bearer {0}".format(self.oauth_token)}

        if headers_new is not None:
            headers.update(headers_new)

        return await self._make_async_request(url=full_url, method=method, headers=headers, json=json, files=files)

    # Helix region ends

    @staticmethod
    def _make_request(url, method: str = 'get', headers: dict = None, json=None, files=None):
        return requests.request(url=url, method=method, json=json, files=files, headers=headers)

    @staticmethod
    async def _make_async_request(url, method: str = 'get', headers: dict = None, json=None, files=None):
        return await requests_async.request(url=url, method=method, json=json, files=files, headers=headers)


