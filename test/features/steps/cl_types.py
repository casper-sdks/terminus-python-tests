import typing

import pycspr.serialisation.utils
import pycspr.types
from behave import *
from pycspr import serialisation, types

from test.features.steps.utils.asyncs import deploy_event, call_async_function
from test.features.steps.utils.deploy import deploy_set_signatures, create_deploy

use_step_matcher("re")


@given('that a CL value of type "(.*)" has a value of "(.*)"')
def that_a_cl_value_of_type_hash_vale(ctx, _type, value):
    print(f'that a CL value of type "{_type}" has a value of "{value}"')

    _cltypes: dict = {'category': 'simple', 'key': _type, 'value': value}

    ctx.cl_types.append(_cltypes)


@then('it\'s bytes will be "(.*)"')
def bytes_will_be(ctx, hex_bytes):
    print(f'it\'s bytes will be "{hex_bytes}"')

    if ctx.cl_types[-1]['category'] == 'simple':

        _type = ctx.values_map[ctx.cl_types[-1]['key']]
        val = get_type(ctx.cl_types[-1]['key'], ctx.cl_types[-1]['value'])
        decoded = get_converted_simple(ctx.cl_types[-1]['key'], _type, val, ctx)

        assert decoded == hex_bytes

    else:

        _type = ctx.values_map[ctx.cl_types[-1]['key']]

        _types_simple: list = []
        for i in ctx.cl_types[-1]['key_simple']:
            _types_simple.append(ctx.values_map[i])

        val: list = []

        for i in range(len(ctx.cl_types[-1]['value'])):
            val.append(get_type(ctx.cl_types[-1]['key_simple'][i], ctx.cl_types[-1]['value'][i]))

        decoded = get_converted_complex(ctx.cl_types[-1]['key'], _type, _types_simple, val, ctx)

        assert decoded == hex_bytes


@given('that the CL complex value of type "(.*)" with an internal types of "(.*)" values of "(.*)"')
def the_complex_type_with_internal_type_has_value(ctx, type_complex, type_internal, value):
    print(
        f'that the CL complex value of type "{type_complex}" with an internal types of "{type_internal}" values of "{value}"')

    _cltypes: dict = {'category': 'complex', 'key': type_complex, 'key_simple': type_internal.split(','),
                      'value': value.split(',')}
    ctx.cl_types.append(_cltypes)


@when("the values are added as arguments to a deploy")
def the_values_are_added_as_arguments_to_a_deploy(ctx):
    print(f'the values are added as arguments to a deploy')

    ctx.user_1 = '1'
    ctx.user_2 = '2'
    ctx.transfer_amount = 2500000000
    ctx.gas_price = 1
    ctx.ttl = '30m'
    ctx.chain = 'casper-net-1'
    ctx.payment_amount = 100000000

    deploy_set_signatures(ctx)

    ctx.deploy = create_deploy(ctx)


@step("the deploy is put on chain")
def the_deploy_is_put_on_chain(ctx):
    print(f'the deploy is put on chain')

    ctx.sdk_client.send_deploy(ctx.deploy)
    ctx.deploy_result = ctx.deploy

    assert ctx.deploy_result.hash.hex()


@step("the deploy has successfully executed")
def the_deploy_has_successfully_executed(ctx):
    print(f'the deploy has successfully executed')

    ctx.timeout = 300
    ctx.execution_result = call_async_function(ctx, deploy_event)

    assert ctx.execution_result[0]['result']['Success']


@when("the deploy is obtained from the node")
def the_deploy_obtained_from_the_node(ctx):
    print(f'the deploy is obtained from the node')

    ctx.deploy = ctx.sdk_client.get_deploy(ctx.deploy_result.hash)
    assert ctx.deploy


@then('the deploys NamedArgument "(.*)" has a value of "(.*)" and bytes of "(.*)"')
def the_deploys_named_args_has_value_and_bytes(ctx, named_arg, _value, _bytes):
    print(f'the deploys NamedArgument "{named_arg}" has a value of "{_value}" and bytes of "{_bytes}"')

    args = ctx.deploy['deploy']['session']['Transfer']['args']
    assert args

    compared = False
    for arg in range(len(args)):
        if args[arg][0] == named_arg:

            if args[arg][1]['cl_type'] == 'Bool':
                assert args[arg][1]['parsed'] == True if _value == 'true' else False
            elif args[arg][1]['cl_type'] == 'URef':
                assert args[arg][1]['parsed'][5:-4] == _value
            else:
                assert compare_value(args[arg][1], _value)

            assert compare_bytes(args[arg][1], _bytes)
            compared = True

    assert compared


def compare_value(arg, value):
    if arg['cl_type'] == 'Key':
        return True
    else:
        return str(arg['parsed']) == str(value)


def compare_bytes(arg, value):
    if arg['cl_type'] == 'Key':
        return str(arg['bytes'])[2:] == str(value)
    else:
        return str(arg['bytes']) == str(value)


@step(
    'the deploys NamedArgument Complex value "(.*)" has internal types of "(.*)" and values of "(.*)" and bytes of "(.*)"')
def step_impl(ctx, complex, internal, _value, _bytes):
    print(
        f'the deploys NamedArgument Complex value "{complex}" has internal types of "{internal}" and values of "{_value}" and bytes of "{_bytes}"')

    args = ctx.deploy['deploy']['session']['Transfer']['args']
    assert args

    _internals: list = internal.split(',')
    _values: list = _value.split(',')

    compared = False
    for arg in range(len(args)):
        if args[arg][0] == complex:

            if complex == 'Map':
                for i in range(len(_values)):
                    assert _values[i] == args[arg][1]['parsed'][i]['value']
                compared = True
            else:
                if isinstance(args[arg][1]['cl_type'][complex], list):
                    assert args[arg][1]['cl_type'][complex] == _internals
                    compared = True
                else:
                    assert args[arg][1]['cl_type'][complex] == _internals[0]
                    compared = True

    assert compared


def get_type(_type, _value):
    if _type in ['U8', 'U32', 'U64', 'U256', 'I32', 'I64']:
        return int(_value)
    elif _type == 'Bool':
        return True if _value == 'true' else False
    else:
        return _value


def get_converted_simple(key, _type, _value, ctx):
    cl_type: types.CL_Value
    args: typing.Dict[str, types.CL_Value]

    if key in ['ByteArray']:
        cl_type = _type(bytes.fromhex(_value))
        args = {key: cl_type}
        ctx.deploy_args.append(args)
        return serialisation.to_bytes(cl_type).hex()
    elif key in ['Key']:
        cl_type = types.CL_Key.from_string('account-hash-' + _value)
        args = {key: cl_type}
        ctx.deploy_args.append(args)
        return cl_type.identifier.hex()
    elif key in ['PublicKey']:
        cl_type = types.CL_PublicKey.from_account_key(bytes.fromhex(_value))
        args = {key: cl_type}
        ctx.deploy_args.append(args)
        return cl_type.account_key.hex()
    elif key in ['URef']:

        cl_type = types.CL_URef(types.CL_URefAccessRights.READ_ADD_WRITE, bytes.fromhex(_value))
        args = {key: cl_type}
        ctx.deploy_args.append(args)

        return str(types.CL_URef(pycspr.types.CL_URefAccessRights.READ_ADD_WRITE, _value).address) + '0' + str(
            types.CL_URef(pycspr.types.CL_URefAccessRights.READ_ADD_WRITE, _value).access_rights.value)

    else:

        cl_type = _type(_value)
        args = {key: cl_type}
        ctx.deploy_args.append(args)

        return serialisation.to_bytes(cl_type).hex()


def get_converted_complex(key, _type_complex, _type_simples, _values, ctx):
    if key in ['Option']:
        ctx.deploy_args.append({key: _type_complex(_type_simples[0](_values[0]), ctx.types_map[_type_simples[0].__name__])})
        return serialisation.to_bytes(_type_complex(_type_simples[0](_values[0]), _type_simples[0])).hex()
    elif key in ['Tuple1']:
        ctx.deploy_args.append({key: _type_complex(_type_simples[0](_values[0]))})
        return serialisation.to_bytes(_type_complex(_type_simples[0](_values[0]))).hex()
    elif key in ['Tuple2']:
        ctx.deploy_args.append({key: _type_complex(_type_simples[0](_values[0]), _type_simples[1](_values[1]))})
        return serialisation.to_bytes(_type_complex(_type_simples[0](_values[0]), _type_simples[1](_values[1]))).hex()
    elif key in ['Tuple3']:
        ctx.deploy_args.append({key: _type_complex(_type_simples[0](_values[0]), _type_simples[1](_values[1]),
                                                   _type_simples[2](_values[2]))})
        return serialisation.to_bytes(_type_complex(_type_simples[0](_values[0]), _type_simples[1](_values[1]),
                                                    _type_simples[2](_values[2]))).hex()
    elif key in ['Map']:
        ctx.deploy_args.append({key: types.CL_Map(build_map(_type_simples, _values))})

        return serialisation.to_bytes(types.CL_Map(build_map(_type_simples, _values))).hex()

    elif key in ['List']:
        cl_list: list = []
        for i in range(len(_type_simples)):
            cl_list.append(_type_simples[i](_values[i]))
        ctx.deploy_args.append({key: _type_complex(cl_list)})
        return serialisation.to_bytes(_type_complex(cl_list)).hex()


def build_map(_type_simples, _values) -> list:

    map_list: list = []
    for i in range(len(_type_simples)):
        _tuple: typing.Tuple = (types.CL_String(str(i)), _type_simples[i](_values[i]))
        map_list.append(_tuple)

    return map_list

