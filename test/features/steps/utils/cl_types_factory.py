import typing

from pycspr.factory import create_public_key_from_account_key
from pycspr.types.cl import *

from test.features.steps.utils.cl_utils import CLTypesUtils


# CL Types factory with methods to create the values and the deploy arguments for later use

class CLTypesFactory:
    _utils = CLTypesUtils()

    def create_value(self, key, _value) -> CLV_Value:

        cl_type: CLV_Value

        _type = CLTypesUtils.cl_values_map[key]
        _value = self._utils.get_type(key, _value)

        if key in ['ByteArray']:
            return _type(bytes.fromhex(_value))

        elif key in ['Key']:
            return CLV_Key.from_str(f'account-hash-{_value}')

        elif key in ['PublicKey']:
            return CLV_PublicKey.from_public_key(create_public_key_from_account_key(bytes.fromhex(_value)))

        elif key in ['URef']:
            return CLV_URef(CLV_URefAccessRights.READ_ADD_WRITE, bytes.fromhex(_value))

        else:
            return _type(_value)

    def create_complex_value(self, key, _type_simples, _values) -> CLV_Value:

        # build a dict list of the type classes and their values
        _simple_types: list = []
        for i in range(len(_type_simples)):
            _simple_types.append({'type': self._utils.cl_values_map[_type_simples[i]],
                                  'value': self._utils.get_type(_type_simples[i], _values[i])})

        if key in ['Option']:
            return CLV_Option(_simple_types[0]['type'](_simple_types[0]['value']),
                              self._utils.cl_types_map[_simple_types[0]['type'].__name__])

        elif key in ['Tuple1']:
            return CLV_Tuple1(_simple_types[0]['type'](_simple_types[0]['value']))

        elif key in ['Tuple2']:
            return CLV_Tuple2(_simple_types[0]['type'](_simple_types[0]['value']),
                              _simple_types[1]['type'](_simple_types[1]['value']))

        elif key in ['Tuple3']:
            return CLV_Tuple3(_simple_types[0]['type'](_simple_types[0]['value']),
                              _simple_types[1]['type'](_simple_types[1]['value']),
                              _simple_types[2]['type'](_simple_types[2]['value']))

        elif key in ['Map']:
            return CLV_Map(self.build_map(_simple_types))

        elif key in ['List']:
            cl_list: list = []
            for i in range(len(_simple_types)):
                cl_list.append(_simple_types[i]['type'](_simple_types[i]['value']))

            return CLV_List(cl_list)

    @staticmethod
    def build_map(_simple_types) -> list:

        map_list: list = []

        for i in range(len(_simple_types)):
            _tuple: typing.Tuple = (CLV_String(str(i)), _simple_types[i]['type'](_simple_types[i]['value']))
            map_list.append(_tuple)

        return map_list
