import os

from pycspr import types

from steps.utils.assets import get_user_asset_path
from steps.utils.config import CONFIG
from steps.utils.exec import NodeExec
from steps.utils.node import *
from steps.utils.requests import NodeRequests

# Steps to run at specific times in the scenarios
# Sets the required context parameters

# CASPER types used for equals comparisons
_cl_values: dict = {
    'Transfer': types.Transfer,
    'U512': types.cl_values.CL_U512,
    'Option': types.cl_values.CL_Option,
    'PublicKey': types.cl_values.CL_PublicKey
}

# Lookups
param_keys: dict = {
    'lastBlockAdded': 'last_block_added'
}


def before_all(ctx):
    ctx.config = CONFIG()
    ctx.sdk_client = client(ctx.config)
    ctx.sdk_client_spec = client_spec(ctx.config)
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
