import json
import os
import re


# Queries the NCTL node

class NCTLExec:
    clean_input = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    def __init__(self, config):
        self.config = config

    def _get_pre_script(self):
        return "docker exec -t " + \
            self.config.get_docker_name() + \
            " /bin/bash -c 'source casper-node/utils/nctl/sh/views/"

    def get_latest_block(self):
        return json.loads(self.clean_input.sub('', os.popen(self._get_pre_script() + "view_chain_block.sh'").read()))

    def get_latest_block_by_param(self, params):
        return json.loads(
            self.clean_input.sub('', os.popen(self._get_pre_script() + "view_chain_block.sh " + params + "'").read()))

    def get_era_switch_block(self):
        return json.loads(self.clean_input.sub('', os.popen(self._get_pre_script() + "view_chain_era_info.sh'").read()))
