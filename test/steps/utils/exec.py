import json
import os
import re


def get_latest_block():
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return json.loads(ansi_escape.sub('', os.popen("docker exec -t storm-nctl /bin/bash -c 'source casper-node/utils/nctl/sh/views/view_chain_block.sh'").read()))
