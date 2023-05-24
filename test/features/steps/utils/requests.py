import json
from time import time

import requests


# NCTL RPC request methods

class NCTLRequests:

    def __init__(self, config):
        self.config = config

    def get_info_get_validator_changes(self):
        return json.loads(self._request('info_get_validator_changes', '[]'))

    def _request(self, method, params) -> str:

        url: str = 'http://' + self.config.get_nctl_host() + ':' + self.config.get_nctl_port_rpc() + "/rpc"
        payload: str = '{"id":"' + str(int(time() * 1000)) + '","jsonrpc":"2.0","method":"' + method + '","params":"' \
                       + params + '"}'
        headers: dict = {'content-type': 'application/json', 'content-length': str(len(payload))}

        return requests.post(url, data=payload, headers=headers).text
