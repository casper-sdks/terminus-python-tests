import os

from pycspr import types

from steps.utils.assets import get_user_asset_path
from steps.utils.config import CONFIG
from steps.utils.exec import NCTLExec
from steps.utils.node import client
from steps.utils.requests import NCTLRequests

# Steps to run at specific times in the scenarios
# Sets the required context parameters

# CASPER types used for equals comparisons
types: dict = {
    'Transfer': types.Transfer,
    'U512': types.cl_values.CL_U512,
    'Option': types.cl_values.CL_Option,
    'PublicKey': types.cl_values.CL_PublicKey,
    'String': types.cl_values.CL_String,
    'U8': types.cl_values.CL_U8,
    'U32': types.cl_values.CL_U32,
    'U64': types.cl_values.CL_U64,
    'U256': types.cl_values.CL_U256,
    'I32': types.cl_values.CL_I32,
    'I64': types.cl_values.CL_I64,
    'Bool': types.cl_values.CL_Bool,
    'ByteArray': types.cl_values.CL_ByteArray,
    'Key': types.cl_values.CL_Key,
    'URef': types.cl_values.CL_URef,
    'Tuple1': types.cl_values.CL_Tuple1,
    'Tuple2': types.cl_values.CL_Tuple2,
    'Tuple3': types.cl_values.CL_Tuple3,
    'List': types.cl_values.CL_List
}


# Lookups
param_keys: dict = {
    'lastBlockAdded': 'last_block_added'
}

cl_types: list = []
# deploy_args: list = []

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
    ctx.cl_types = cl_types
    ctx.deploy_args = []
    ctx.user_1 = '1'
    ctx.user_2 = '2'
