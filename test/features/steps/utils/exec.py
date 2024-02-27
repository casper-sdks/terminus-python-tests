import json
import os
import re
import subprocess


# Queries the CCTL node

class NodeExec:
    _clean_input = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    def __init__(self, config):
        self.config = config

    def _get_pre_script(self):
        return "docker exec -t " + self.config.get_docker_name() + " /bin/bash -c -i '"

    def get_latest_block(self):
        return json.loads(self._clean_input.sub('', os.popen(self._get_pre_script() + "cctl-chain-view-block'").read()))

    def get_latest_block_by_param(self, params):
        return json.loads(
            self._clean_input.sub('', os.popen(self._get_pre_script() + "cctl-chain-view-block " + params + "'").read()))

    def get_user_account(self, params):
        res = os.popen(self._get_pre_script() + "cctl-chain-view-account-of-user " + params + "'").read()
        return json.loads(self._clean_input.sub('', res[res.find('{'):len(res)]))

    def get_era_summary(self):
        return json.loads(
            self._clean_input.sub('', os.popen(self._get_pre_script() + "cctl-chain-view-era-summary'").read()))

    # view_node_status returns a console line followed by json
    # the method will return just the json
    def get_node_status(self, node):
        res = os.popen(self._get_pre_script() + "cctl-infra-node-view-status node=" + str(node) + "'").read()
        return json.loads(self._clean_input.sub('', res[res.find('{'):len(res)]))

    # view_chain_state_root_hash returns non json output
    # the method returns the whole line for comparison
    def get_state_root_hash(self, node):
        try:
            res = os.popen(self._get_pre_script() + "cctl-chain-view-state-root-hash'").read()
            nodes = res.split("\n")
            return nodes[node-1].split("=")[1].split()[0]

        except Exception as err:
            raise Exception(f'Error getting State Root Hash from node {node} CCTL {res} {err}')

    def get_account_main_purse(self, params):
        res = os.popen(self._get_pre_script() + "cctl-chain-view-account-of-user " + params + "'").read()
        return json.loads(self._clean_input.sub('',
                                                res[res.find('{'):len(res)]))['main_purse']
