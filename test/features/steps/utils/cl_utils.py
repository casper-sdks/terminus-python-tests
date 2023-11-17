from pycspr import types, serialisation


# Helper file to hold CL Type short name and class name lookups

class CLTypesUtils:
    cl_types_map: dict = {
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

    cl_values_map: dict = {
        'Transfer': types.Transfer,
        'U512': types.CL_U512,
        'U128': types.CL_U128,
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

    @staticmethod
    def get_type(_type, _value):
        if _type in ['U8', 'U32', 'U64', 'U256', 'I32', 'I64']:
            return int(_value)
        elif _type == 'Bool':
            return True if _value == 'true' else False
        else:
            return _value

    @staticmethod
    def to_hex_bytes(cl_type: dict):

        _type = list(cl_type.items())[0][0]
        _cl_type = list(cl_type.items())[0][1]

        if _type in ['Key']:
            return _cl_type.identifier.hex()
        elif _type in ['PublicKey']:
            return _cl_type.account_key.hex()
        elif _type in ['URef']:
            return serialisation.to_bytes(_cl_type).hex()
        else:
            return serialisation.to_bytes(_cl_type).hex()
