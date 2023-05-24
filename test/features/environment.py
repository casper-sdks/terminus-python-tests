import os

import pycspr.types

from steps.utils.assets import get_user_asset_path
from steps.utils.config import CONFIG
from steps.utils.exec import NCTLExec
from steps.utils.node import client
from steps.utils.requests import NCTLRequests

# Steps to run at specific times in the scenarios
# Sets the required context parameters

# CASPER types used for equals comparisons
types: dict = {
    'Transfer': pycspr.types.Transfer,
    'U512': pycspr.types.cl_values.CL_U512,
    'Option': pycspr.types.cl_values.CL_Option,
    'PublicKey': pycspr.types.cl_values.CL_PublicKey
}

# Lookups
param_keys: dict = {
    'lastBlockAdded': 'last_block_added'
}


def before_all(ctx):
    ctx.config = CONFIG()
    ctx.sdk_client = client(ctx.config)
    ctx.nctl_client = NCTLExec(ctx.config)
    ctx.nctl_requests = NCTLRequests(ctx.config)
    ctx.ASSETS_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../assets/'))
    ctx.get_user_asset_path = get_user_asset_path
    ctx.param_map = {}
    ctx.param_keys = param_keys
    ctx.types_map = types
