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
_cl_values: dict = {
    'Transfer': types.Transfer,
    'U512': types.CL_U512,
    'Option': types.CL_Option,
    'PublicKey': types.CL_PublicKey,
    'String': types.CL_String,
    'U8': types.CL_U8,
    'U32': types.CL_U32,
    'U64': types.CL_U64,
    'U256': types.CL_U256,
    'I32': types.CL_I32,
    'I64': types.CL_I64,
    'Bool': types.CL_Bool,
    'ByteArray': types.CL_ByteArray,
    'Key': types.CL_Key,
    'URef': types.CL_URef,
    'Tuple1': types.CL_Tuple1,
    'Tuple2': types.CL_Tuple2,
    'Tuple3': types.CL_Tuple3,
    'List': types.CL_List,
    'Map': types.CL_Map
}

_cl_types: dict = {
    'CL_U512': types.CL_Type_U512,
    'CL_Option': types.CL_Type_Option,
    'CL_PublicKey': types.CL_Type_PublicKey,
    'CL_String': types.CL_Type_String,
    'CL_U8': types.CL_Type_U8,
    'CL_U32': types.CL_Type_U32,
    'CL_U64': types.CL_Type_U64,
    'CL_U256': types.CL_Type_U256,
    'CL_I32': types.CL_Type_I32,
    'CL_I64': types.CL_Type_I64,
    'CL_Bool': types.CL_Type_Bool,
    'CL_ByteArray': types.CL_Type_ByteArray,
    'CL_Key': types.CL_Type_Key,
    'CL_URef': types.CL_Type_URef,
    'CL_Tuple1': types.CL_Type_Tuple1,
    'CL_Tuple2': types.CL_Type_Tuple2,
    'CL_Tuple3': types.CL_Type_Tuple3,
    'CL_List': types.CL_Type_List,
    'CL_Map': types.CL_Type_Map
}


# Lookups
param_keys: dict = {
    'lastBlockAdded': 'last_block_added'
}

cl_types: list = []
cl_types_complex: list = []

def before_all(ctx):
    ctx.config = CONFIG()
    ctx.sdk_client = client(ctx.config)
    ctx.nctl_client = NCTLExec(ctx.config)
    ctx.nctl_requests = NCTLRequests(ctx.config)
    ctx.ASSETS_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../assets/'))
    ctx.get_user_asset_path = get_user_asset_path
    ctx.param_map = {}
    ctx.param_keys = param_keys
    ctx.values_map = _cl_values
    ctx.types_map = _cl_types
    ctx.cl_types = cl_types
    ctx.cl_types_complex = cl_types_complex
    ctx.deploy_args = []
    ctx.user_1 = '1'
    ctx.user_2 = '2'
