import json
from time import time

import requests


# NCTL RPC request methods

class NCTLRequests:

    def __init__(self, config):
        self.config = config

    def get_info_get_validator_changes(self):
        return json.loads(self._request('info_get_validator_changes', '[]'))

    def get_chain_spec(self):
        return json.loads(self._request('info_get_chainspec', '[]'))

    def get_state_get_auction_info(self, hash):
        return json.loads(self._request('state_get_auction_info', '[{\"Hash\":  \"' + hash + '\"}]'))

    def get_state_get_balance(self, state_root_hash, purse_uref):
        return json.loads(self._request('state_get_balance', '{\"state_root_hash\":\"' + state_root_hash + '\",\"purse_uref\":\"' + purse_uref + '\"}'))

    def _request(self, method, params) -> str:

        url: str = 'http://' + self.config.get_nctl_host() + ':' + self.config.get_nctl_port_rpc() + "/rpc"
        payload: str = '{"id":"' + str(int(time() * 1000)) + '","jsonrpc":"2.0","method":"' + method + '","params":' \
                       + params + '}'
        headers: dict = {'content-type': 'application/json', 'content-length': str(len(payload))}

        return requests.post(url, data=payload, headers=headers).text
