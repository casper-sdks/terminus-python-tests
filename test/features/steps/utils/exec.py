import json
import os
import re


class NCTLExec:
    clean_input = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    def get_latest_block(self):
        return json.loads(self.clean_input.sub('',
                                               os.popen(
                                                   "docker exec -t storm-nctl /bin/bash -c 'source "
                                                   "casper-node/utils/nctl/sh/views/view_chain_block.sh'").read()))

    def get_latest_block_by_param(self, params):
        return json.loads(self.clean_input.sub('',
                                               os.popen(
                                                   "docker exec -t storm-nctl /bin/bash -c 'source "
                                                   "casper-node/utils/nctl/sh/views/view_chain_block.sh block=" + params + "'").read()))
