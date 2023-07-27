import pycspr.serialisation.utils
import pycspr.types
from behave import *
from pycspr import serialisation, types

from test.features.steps.utils.deploy import deploy_set_signatures, deploy_to_chain

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

        _type = ctx.types_map[ctx.cl_types[-1]['key']]
        val = get_type(ctx.cl_types[-1]['key'], ctx.cl_types[-1]['value'])
        decoded = get_converted_simple(ctx.cl_types[-1]['key'], _type, val)

        assert decoded == hex_bytes

    else:

        _type_complex = ctx.types_map[ctx.cl_types[-1]['key']]

        _types_simple: list = []
        for i in ctx.cl_types[-1]['key_simple']:
            _types_simple.append(ctx.types_map[i])

        val: list = []

        for i in range(len(ctx.cl_types[-1]['value'])):
            val.append(get_type(ctx.cl_types[-1]['key_simple'][i], ctx.cl_types[-1]['value'][i]))

        decoded = get_converted_complex(ctx.cl_types[-1]['key'], _type_complex, _types_simple, val)

        assert decoded == hex_bytes


@given('that the CL complex value of type "(.*)" with an internal types of "(.*)" values of "(.*)"')
def the_complex_type_with_internal_type_has_value(ctx, type_complex, type_internal, value):
    print(
        f'that the CL complex value of type "{type_complex}" with an internal types of "{type_internal}" values of "{value}"')

    _cltypes: dict = {'category': 'complex', 'key': type_complex, 'key_simple': type_internal.split(','), 'value': value.split(',')}
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
    ctx.deploy_result = deploy_to_chain(ctx)




@step("the deploy is put on chain")
def the_deploy_is_put_on_chain(ctx):
    print(f'the deploy is put on chain')


@step("the deploy has successfully executed")
def the_deploy_has_successfully_executed(ctx):
    print(f'the deploy has successfully executed')


@when("the deploy is obtained from the node")
def step_impl(ctx):
    print(f'the deploy is obtained from the node')


@then('the deploys NamedArgument "(.*)" has a value of "(.*)" and bytes of "(.*)"')
def the_deploys_named_args_has_value_and_bytes(ctx, named_arg, _value, _bytes):
    print(f'the deploys NamedArgument "{named_arg}" has a value of "{_value}" and bytes of "{_bytes}"')


@step(
    'the deploys NamedArgument Complex value "(.*)" has internal types of "(.*)" and values of "(.*)" and bytes of "(.*)"')
def step_impl(ctx, complex, internal, _value, _bytes):
    print(
        f'the deploys NamedArgument Complex value "{complex}" has internal types of "{internal}" and values of "{_value}" and bytes of "{_bytes}"')


def get_type(_type, _value):
    if _type in ['U8', 'U32', 'U64', 'U256', 'I32', 'I64']:
        return int(_value)
    elif _type == 'Bool':
        return True if _value == 'true' else False
    else:
        return _value

def get_converted_simple(key, _type, _value):

    if key in ['ByteArray']:
        return serialisation.to_bytes(_type(_value))
    elif key in ['Key']:
        return _type(_value, types.PublicKey).identifier
    elif key in ['PublicKey']:
        return types.CL_PublicKey(pycspr.KeyAlgorithm.ED25519, _value).pbk
    elif key in ['URef']:

        # str(types.CL_URef(pycspr.types.CL_URefAccessRights.READ_ADD_WRITE, _value).address) + '0' + str(
        #     types.CL_URef(pycspr.types.CL_URefAccessRights.READ_ADD_WRITE, _value).access_rights.value)

        return types.CL_URef(pycspr.types.CL_URefAccessRights.READ_ADD_WRITE, _value)
    else:
        return serialisation.to_bytes(_type(_value)).hex()

def get_converted_complex(key, _type_complex, _type_simples, _values):

    if key in ['Option']:
        return serialisation.to_bytes(_type_complex(_type_simples[0](_values[0]), _type_simples[0])).hex()
    elif key in ['Tuple1']:
        return serialisation.to_bytes(_type_complex(_type_simples[0](_values[0]))).hex()
    elif key in ['Tuple2']:
        return serialisation.to_bytes(_type_complex(_type_simples[0](_values[0]), _type_simples[1](_values[1]))).hex()
    elif key in ['Tuple3']:
        return serialisation.to_bytes(_type_complex(_type_simples[0](_values[0]), _type_simples[1](_values[1]), _type_simples[2](_values[2]))).hex()
    elif key in ['List']:
        cl_list: list = []
        for i in range(len(_type_simples)):
            cl_list.append(_type_simples[i](_values[i]))

        return serialisation.to_bytes(_type_complex(cl_list)).hex()
