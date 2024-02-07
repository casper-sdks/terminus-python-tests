import json
import os
import re
import subprocess


# Queries the NCTL node

class NCTLExec:
    _clean_input = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    _source: str = 'source casper-node/utils/nctl/script/views/'

    def __init__(self, config):
        self.config = config

    def _get_pre_script(self):
        return "docker exec -t " + self.config.get_docker_name() + " /bin/bash -c '" + self._source

    def get_latest_block(self):
        return json.loads(self._clean_input.sub('', os.popen(self._get_pre_script() + "view_chain_block.script'").read()))

    def get_latest_block_by_param(self, params):
        return json.loads(
            self._clean_input.sub('', os.popen(self._get_pre_script() + "view_chain_block.script " + params + "'").read()))

    def get_user_account(self, params):
        res = os.popen(self._get_pre_script() + "view_user_account.script " + params + "'").read()
        return json.loads(self._clean_input.sub('', res[res.find('{'):len(res)]))

    def get_era_switch_block(self):
        return json.loads(
            self._clean_input.sub('', os.popen(self._get_pre_script() + "view_chain_era_info.script'").read()))

    # view_node_status returns a console line followed by json
    # the method will return just the json
    def get_node_status(self, node):
        res = os.popen(self._get_pre_script() + "view_node_status.script node=" + str(node) + "'").read()
        return json.loads(self._clean_input.sub('', res[res.find('{'):len(res)]))

    # view_chain_state_root_hash returns non json output
    # the method returns the whole line for comparison
    def get_state_root_hash(self, node):
        res = subprocess.check_output(["docker", "exec", "-t", self.config.get_docker_name(), '/bin/bash', "-c",
                                       self._source + "view_chain_state_root_hash.script node="
                                       + str(node)]).decode('utf-8')

        return res.split("=")[1].split()[0]

    def get_account_main_purse(self, params):
        res = os.popen(self._get_pre_script() + "view_user_account.script " + params + "'").read()
        return json.loads(self._clean_input.sub('',
                                                res[res.find('{'):len(res)]))['stored_value']['Account']['main_purse']

    def get_account_balance(self, params):
        res = subprocess.check_output(["docker", "exec", "-t", self.config.get_docker_name(), '/bin/bash', "-c",
                                       self._source + "view_chain_balance.script "
                                       + str(params)]).decode('utf-8')

        try:
            return int(res.split("=")[1].split()[0])
        except Exception as err:
            raise Exception(f'Error getting account balance from NCTL {res} {err}')
