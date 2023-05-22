import json
import os
import re
import subprocess


# Queries the NCTL node

class NCTLExec:
    _clean_input = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    _source: str = 'source casper-node/utils/nctl/sh/views/'

    def __init__(self, config):
        self.config = config

    def _get_pre_script(self):
        return "docker exec -t " + self.config.get_docker_name() + " /bin/bash -c '" + self._source

    def get_latest_block(self):
        return json.loads(self._clean_input.sub('', os.popen(self._get_pre_script() + "view_chain_block.sh'").read()))

    def get_latest_block_by_param(self, params):
        return json.loads(
            self._clean_input.sub('', os.popen(self._get_pre_script() + "view_chain_block.sh " + params + "'").read()))

    def get_era_switch_block(self):
        return json.loads(self._clean_input.sub('', os.popen(self._get_pre_script() + "view_chain_era_info.sh'").read()))

    def get_state_root_hash(self, node):

        res = subprocess.check_output(["docker", "exec", "-t", self.config.get_docker_name(), '/bin/bash', "-c",
                                       self._source + "view_chain_state_root_hash.sh node="
                                       + str(node)]).decode('utf-8')

        return res.split("=")[1].split()

