import typing

from pycspr import types, serialisation

from test.features.steps.utils.cl_maps import CLTypesUtils


# CL Types factory with methods to create the values and the deploy arguments for later use

class CLTypesFactory:
    _utils = CLTypesUtils()

    def create_value(self, key, _value, ctx):

        cl_type: types.CL_Value

        _type = CLTypesUtils.cl_values_map[key]
        _value = self.get_type(key, _value)

        if key in ['ByteArray']:

            cl_type = _type(bytes.fromhex(_value))
            ctx.deploy_args.append({key: _type(bytes.fromhex(_value))})

            return serialisation.to_bytes(cl_type).hex()

        elif key in ['Key']:

            cl_type = types.CL_Key.from_string('account-hash-' + _value)
            ctx.deploy_args.append({key: cl_type})

            return cl_type.identifier.hex()

        elif key in ['PublicKey']:

            cl_type = types.CL_PublicKey.from_account_key(bytes.fromhex(_value))
            ctx.deploy_args.append({key: cl_type})

            return cl_type.account_key.hex()

        elif key in ['URef']:

            cl_type = types.CL_URef(types.CL_URefAccessRights.READ_ADD_WRITE, bytes.fromhex(_value))
            ctx.deploy_args.append({key: cl_type})

            return str(types.CL_URef(types.CL_URefAccessRights.READ_ADD_WRITE, _value).address) + '0' + str(
                types.CL_URef(types.CL_URefAccessRights.READ_ADD_WRITE, _value).access_rights.value)

        else:

            cl_type = _type(_value)
            ctx.deploy_args.append({key: cl_type})

            return serialisation.to_bytes(cl_type).hex()

    def create_complex_value(self, key, _type_simples, _values, ctx):

        # build a dict list of the type classes and their values
        _simple_types: list = []
        for i in range(len(_type_simples)):
            _simple_types.append({'type': self._utils.cl_values_map[_type_simples[i]],
                                  'value': self.get_type(_type_simples[i], _values[i])})

        if key in ['Option']:

            ctx.deploy_args.append(
                {key: types.CL_Option(_simple_types[0]['type'](_simple_types[0]['value']),
                                      self._utils.cl_types_map[_simple_types[0]['type'].__name__])})

            return serialisation.to_bytes(types.CL_Option(_simple_types[0]['type']((_simple_types[0]['value'])),
                                                          _simple_types[0]['type'])).hex()

        elif key in ['Tuple1']:

            ctx.deploy_args.append({key: types.CL_Tuple1(_simple_types[0]['type'](_simple_types[0]['value']))})

            return serialisation.to_bytes(types.CL_Tuple1(_simple_types[0]['type'](_simple_types[0]['value']))).hex()

        elif key in ['Tuple2']:

            ctx.deploy_args.append({key: types.CL_Tuple2(_simple_types[0]['type'](_simple_types[0]['value']),
                                                         _simple_types[1]['type'](_simple_types[1]['value']))})

            return serialisation.to_bytes(
                types.CL_Tuple2(_simple_types[0]['type'](_simple_types[0]['value']),
                                _simple_types[1]['type'](_simple_types[1]['value']))).hex()

        elif key in ['Tuple3']:

            ctx.deploy_args.append({key: types.CL_Tuple3(_simple_types[0]['type'](_simple_types[0]['value']),
                                                         _simple_types[1]['type'](_simple_types[1]['value']),
                                                         _simple_types[2]['type'](_simple_types[2]['value']))})

            return serialisation.to_bytes(types.CL_Tuple3(_simple_types[0]['type'](_simple_types[0]['value']),
                                                          _simple_types[1]['type'](_simple_types[1]['value']),
                                                          _simple_types[2]['type'](_simple_types[2]['value']))).hex()

        elif key in ['Map']:

            ctx.deploy_args.append({key: types.CL_Map(self.build_map(_simple_types))})

            return serialisation.to_bytes(types.CL_Map(self.build_map(_simple_types))).hex()

        elif key in ['List']:

            cl_list: list = []
            for i in range(len(_simple_types)):
                cl_list.append(_simple_types[i]['type'](_simple_types[i]['value']))
            ctx.deploy_args.append({key: types.CL_List(cl_list)})
            return serialisation.to_bytes(types.CL_List(cl_list)).hex()

    @staticmethod
    def build_map(_simple_types) -> list:

        map_list: list = []

        for i in range(len(_simple_types)):
            _tuple: typing.Tuple = (types.CL_String(str(i)), _simple_types[i]['type'](_simple_types[i]['value']))
            map_list.append(_tuple)

        return map_list

    @staticmethod
    def get_type(_type, _value):
        if _type in ['U8', 'U32', 'U64', 'U256', 'I32', 'I64']:
            return int(_value)
        elif _type == 'Bool':
            return True if _value == 'true' else False
        else:
            return _value
