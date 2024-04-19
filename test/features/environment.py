import os


from pycspr.types.cl import CLT_Type_U512, CLT_Type_Option, CLT_Type_PublicKey


from test.features.steps.utils.assets import get_user_asset_path
from test.features.steps.utils.config import CONFIG
from test.features.steps.utils.node import client_rpc, client_sse, client_spec
from test.features.steps.utils.scripts import NodeExec
from test.features.steps.utils.requests import NodeRequests

# Steps to run at specific times in the scenarios
# Sets the required context parameters

# CASPER types used for equals comparisons
_cl_values: dict = {
    # 'Transfer': types.Transfer,
    'U512':  CLT_Type_U512,
    'Option': CLT_Type_Option,
    'PublicKey': CLT_Type_PublicKey
}

# Lookups
param_keys: dict = {
    'lastBlockAdded': 'last_block_added'
}


def before_all(ctx):
    ctx.config = CONFIG()
    ctx.sdk_client_rpc = client_rpc(ctx.config)
    ctx.sdk_client_sse = client_sse(ctx.config)
    ctx.sdk_client_spec = client_spec(ctx.config)
    ctx.chain_name = CONFIG().get_node_chain_name()
    ctx.node_client = NodeExec(ctx.config)
    ctx.node_requests = NodeRequests(ctx.config)
    ctx.ASSETS_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../assets/'))
    ctx.get_user_asset_path = get_user_asset_path
    ctx.param_map = {}
    ctx.param_keys = param_keys
    ctx.values_map = _cl_values
    ctx.cl_values = []
    ctx.deploy_args = []
    ctx.user_1 = '1'
    ctx.user_2 = '2'
