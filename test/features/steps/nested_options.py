import typing

from behave import *
from pycspr import types, serialisation

from test.features.steps.utils.asyncs import deploy_event, call_async_function
from test.features.steps.utils.cl_types_factory import CLTypesFactory
from test.features.steps.utils.cl_utils import CLTypesUtils
from test.features.steps.utils.deploy import deploy_set_signatures, create_deploy

use_step_matcher("re")

_factory = CLTypesFactory()
_utils = CLTypesUtils()


# Step Definitions for Nested CL Type Option Cucumber Tests

@given(
    'that a nested Option has an inner type of Option with a type of (.*) and a value of "(.*)"')
def nested_option_created(ctx, _type, _value):
    print(f'that a nested Option has an inner type of Option with a type of {_type} and a value of "{_value}"')

    __type = _utils.cl_values_map[_type]
    __val = __type(_value)

    ctx.cl_option = types.CL_Option(types.CL_Option(__val, _utils.cl_types_map['CL_Option']),
                                    _utils.cl_types_map['CL_' + _type])

    assert ctx.cl_option


@then('the inner type is Option with a type of (.*) and a value of "(.*)"')
def nested_option_has_values(ctx, _type_inner, _value):
    print(f'the inner type is Option with a type of {_type_inner} and a value of "{_value}"')

    """
    The test will fail here when checking the CL_Type from the Deploy
    The CL_Type needs to be serialised into a CL_Type object
    """

    assert isinstance(ctx.cl_option, types.CL_Option)
    assert isinstance(ctx.cl_option.value.value, _utils.cl_values_map[_type_inner])
    assert ctx.cl_option.value.value.value == _value


@step('the bytes are "(.*)"')
def bytes_are(ctx, hex_bytes):
    print(f'the bytes are "{hex_bytes}"')

    """
    The test will fail here when checking the CL_Type from the Deploy
    The CL_Type needs to be serialised into a CL_Type object
    """

    assert serialisation.to_bytes(ctx.cl_option).hex() == hex_bytes


@given("that the nested Option is deployed in a transfer")
def is_deployed(ctx):
    print(f'that the nested Option is deployed in a transfer')
    deploy_nested_option(ctx)


@step("the transfer containing the nested Option is successfully executed")
def deploy_successful(ctx):
    print(f'the transfer containing the nested Option is successfully executed')

    ctx.timeout = 300
    ctx.execution_result = call_async_function(ctx, deploy_event)
    assert ctx.execution_result[0]['result']['Success']


@given("that a nested Option has an inner type of List with a type of (.*) and a value of \((.*), (.*), (.*)\)")
def option_list_has_values(ctx, _type, _val1, _val2, _val3):
    print(f'that a nested Option has an inner type of List with a type of {_type} and a value of \({_val1}, {_val1}, {_val1}\)')

    """
    This test passes, but fails to deploy
    AttributeError: type object 'CL_Type_List' has no attribute 'inner_type'    
    The SDK is not checking for nested complex cl_types in the CL_Option_type 
    """

    _list = [_factory.create_value(_type, _val1),
             _factory.create_value(_type, _val2),
             _factory.create_value(_type, _val3)]

    ctx.cl_list = types.CL_List(_list)

    ctx.cl_option = types.CL_Option(types.CL_List(_list), types.CL_Type_List)

    assert ctx.cl_option
    assert isinstance(ctx.cl_option.value, types.CL_List)

    ctx.cl_list = ctx.cl_option.value
    assert ctx.cl_list


@given(
    'that a nested Option has an inner type of Tuple2 with a type of "(.*),(.*)" values of "(.*),(.*)"')
def option_tuple_is_created(ctx, _type1, _type2, _val1, _val2):
    print(f'that a nested Option has an inner type of Tuple2 with a type of "{_type1},{_type2}" values of "{_val1},{_val2}"')

    """
    This test passes, but fails to deploy
    AttributeError: type object 'CL_Type_Tuple2' has no attribute 't0_type'
    The SDK is not checking for nested complex cl_types in the CL_Option_type    
    """

    __type1 = _utils.cl_values_map[_type1]
    __type2 = _utils.cl_values_map[_type2]
    __val1 = _factory.create_value(_type1, _utils.get_type(__type1, _val1))
    __val2 = _factory.create_value(_type2, _utils.get_type(__type2, _val2))

    _tuple = types.CL_Tuple2(__val1, __val2)

    ctx.cl_option = types.CL_Option(_tuple, _utils.cl_types_map['CL_Tuple2'])

    assert ctx.cl_option


@then(
    'the inner type is Tuple2 with a type of "(.*),(.*)" and a value of "(.*), (.*)"')
def option_tupke_has_values(ctx, _type1, _type2, _val1, _val2):
    print(f'the inner type is Tuple2 with a type of "{_type1},{_type2}" and a value of "{_val1},{_val2}"')

    """
    The test will fail here when checking the CL_Type from the Deploy
    The CL_Type needs to be serialised into a CL_Type object
    """

    assert isinstance(ctx.cl_option.value.v0, _utils.cl_values_map[_type1])
    assert isinstance(ctx.cl_option.value.v1, _utils.cl_values_map[_type2])

    assert ctx.cl_option.value.v0.value == _utils.get_type(_type1, _val1)
    assert ctx.cl_option.value.v1.value == _utils.get_type(_type2, _val2)


@given('that a nested Option has an inner type of Map with a type of "(.*),(.*)" values of "\{"(.*)": (.*)\}"')
def option_map_has_values(ctx, _type1, _type2, _val1, _val2):
    print(
        f'that a nested Option has an inner type of Map with a type of "{_type1},{_type2}" values of "{_val1},{_val2}"')

    """
    This test passes, but fails to deploy
    AttributeError: type object 'CL_Type_Map' has no attribute 'key_type'
    The SDK is not checking for nested complex cl_types in the CL_Option_type 
    """

    _list = []
    _tuple: typing.Tuple = (types.CL_String(_val1), types.CL_U32(int(_val2)))
    _list.append(_tuple)

    _map = types.CL_Map(_list)

    ctx.cl_option = types.CL_Option(_map, _utils.cl_types_map['CL_Map'])

    assert ctx.cl_option


@then('the inner type is Map with a type of "(.*),(.*)" and a value of "\{"(.*)": (.*)\}"')
def option_map_created(ctx, _type1, _type2, _val1, _val2):
    print(f'the inner type is Map with a type of "{_type1},{_type2}" and a value of "{_val1},{_val2}"')

    """
    The test will fail here when checking the CL_Type from the Deploy
    The CL_Type needs to be serialised into a CL_Type object
    """

    assert isinstance(ctx.cl_option, types.cl_values.CL_Option)
    assert isinstance(ctx.cl_option.value, types.CL_Map)
    assert isinstance(ctx.cl_option.value.value[0][0], types.CL_String)
    assert isinstance(ctx.cl_option.value.value[0][1], types.CL_U32)
    assert ctx.cl_option.value.value[0][0].value == _val1
    assert ctx.cl_option.value.value[0][1].value == int(_val2)


@given('that a nested Option has an inner type of Any with a value of "(.*)"')
def option_any_created(ctx, _value):
    print(f'that a nested Option has an inner type of Any with a value of "{_value}"')

    """
    This test passes, but fails to encode
    CL_Any encoding 'NotImplemented' in the SDK
    """

    ctx.cl_option = types.CL_Option(types.CL_Any(types.CL_String(_value)), types.CL_Any)

    assert ctx.cl_option


@then('the inner type is Any with a value of "(.*)"')
def inner_type_is_any(ctx, _value):
    print(f'the inner type is Any with a value of "{_value}"')

    assert isinstance(ctx.cl_option, types.cl_values.CL_Option)
    assert isinstance(ctx.cl_option.value, types.cl_values.CL_Any)
    assert isinstance(ctx.cl_option.value.value, types.CL_String)
    assert ctx.cl_option.value.value.value == _value


def deploy_nested_option(ctx):
    ctx.user_1 = '1'
    ctx.user_2 = '2'
    ctx.transfer_amount = 2500000000
    ctx.gas_price = 1
    ctx.ttl = '30m'
    ctx.chain = 'cspr-dev-cctl'
    ctx.payment_amount = 100000000

    ctx.cl_values = []
    ctx.cl_values.append({'OPTION': ctx.cl_option})

    ctx.cl_option = ""

    deploy_set_signatures(ctx)

    ctx.deploy = create_deploy(ctx)

    ctx.sdk_client.send_deploy(ctx.deploy)
    ctx.deploy_result = ctx.deploy

    assert ctx.deploy_result.hash.hex()
