from pycspr.types.cl import *
from pycspr.serializer import to_bytes

# Helper file to hold CL Type short name and class name lookups

class CLTypesUtils:
    cl_types_map: dict = {
        'CLV_U512': CLT_Type_U512,
        'CLV_Option': CLT_Type_Option,
        'CLV_PublicKey': CLT_Type_PublicKey,
        'CLV_String': CLT_Type_String,
        'CLV_U8': CLT_Type_U8,
        'CLV_U32': CLT_Type_U32,
        'CLV_U64': CLT_Type_U64,
        'CLV_U128': CLT_Type_U128,
        'CLV_U256': CLT_Type_U256,
        'CLV_I32': CLT_Type_I32,
        'CLV_I64': CLT_Type_I64,
        'CLV_Bool': CLT_Type_Bool,
        'CLV_ByteArray': CLT_Type_ByteArray,
        'CLV_Key': CLT_Type_Key,
        'CLV_URef': CLT_Type_URef,
        'CLV_Tuple1': CLT_Type_Tuple1,
        'CLV_Tuple2': CLT_Type_Tuple2,
        'CLV_Tuple3': CLT_Type_Tuple3,
        'CLV_List': CLT_Type_List,
        'CLV_Map': CLT_Type_Map,
        'CLV_Any': CLT_Type_Any
    }

    cl_values_map: dict = {
        # 'Transfer': Transfer,
        'U512': CLV_U512,
        'U128': CLV_U128,
        'Option': CLV_Option,
        'PublicKey': CLV_PublicKey,
        'String': CLV_String,
        'U8': CLV_U8,
        'U32': CLV_U32,
        'U64': CLV_U64,
        'U256': CLV_U256,
        'I32': CLV_I32,
        'I64': CLV_I64,
        'Bool': CLV_Bool,
        'ByteArray': CLV_ByteArray,
        'Key': CLV_Key,
        'URef': CLV_URef,
        'Tuple1': CLV_Tuple1,
        'Tuple2': CLV_Tuple2,
        'Tuple3': CLV_Tuple3,
        'List': CLV_List,
        'Map': CLV_Map,
        'Any': CLV_Any
    }

    @staticmethod
    def get_type(_type, _value):
        if _type in ['U8', 'U32', 'U64', 'U128', 'U256', 'U512', 'I32', 'I64']:
            return int(_value)
        elif _type == 'Bool':
            return True if _value == 'true' else False
        else:
            return _value

    @staticmethod
    def to_hex_bytes(CLV_type: dict):

        _type = list(CLV_type.items())[0][0]
        _CLV_type = list(CLV_type.items())[0][1]

        if _type in ['Key']:
            return _CLV_type.identifier.hex()
        elif _type in ['PublicKey']:
            return _CLV_type.account_key.hex()
        elif _type in ['URef']:
            return to_bytes(_CLV_type).hex()
        else:
            return to_bytes(_CLV_type).hex()
