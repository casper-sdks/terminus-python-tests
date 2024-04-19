import typing

from behave import *
from pycspr.types.cl import *
from pycspr.serializer import to_bytes

from test.features.steps.utils.asyncs import call_async_function, deploy_event
from test.features.steps.utils.cl_types_factory import CLTypesFactory
from test.features.steps.utils.cl_utils import CLTypesUtils
from test.features.steps.utils.deploy import deploy_set_signatures, create_deploy

_factory = CLTypesFactory()
_utils = CLTypesUtils()

use_step_matcher("re")

# Step Definitions for Nested Maps CL Types Cucumber Tests


@given('a map is created \{"(.*)": (.*)\}')
def a_map_is_created(ctx, key, value):
    print(f'a map is created {key}:{value}')

    _list = []
    _tuple: typing.Tuple = (CLV_String(key), CLV_U32(int(value)))
    _list.append(_tuple)
    ctx.CLV_map = CLV_Map(_list)


@then('the map\'s key type is "(.*)" and the maps value type is "(.*)"')
def map_has_value(ctx, key1, key2):
    print(f'the map\'s key type is "{key1}" and the maps value type is "{key2}"')

    """
    The test will fail here when checking the CLV_Type from the Deploy
    The CLV_Type needs to be serialised into a CLV_Type object
    """

    assert isinstance(ctx.CLV_map.value[0][0], _utils.cl_values_map[key1])
    assert isinstance(ctx.CLV_map.value[0][1], _utils.cl_values_map[key2])


@then('the map\'s bytes are "(.*)"')
def map_has_bytes(ctx, hex_bytes):
    print(f'the map\'s bytes are "{hex_bytes}"')

    """
    The test will fail here when checking the CLV_Type from the Deploy
    The CLV_Type needs to be serialised into a CLV_Type object
    """
    assert to_bytes(ctx.CLV_map).hex() == hex_bytes


@given("that the nested map is deployed in a transfer")
def map_is_deployed(ctx):
    print(f'that the nested map is deployed in a transfer')

    deploy_map(ctx)


@step("the transfer containing the nested map is successfully executed")
def map_is_deployed_successfully(ctx):
    print(f'the transfer containing the nested map is successfully executed')

    ctx.timeout = 300
    ctx.execution_result = call_async_function(ctx, deploy_event)
    assert ctx.execution_result[0]['result']['Success']


@when("the map is read from the deploy")
def map_is_read_from_the_deploy(ctx):
    print(f'the map is read from the deploy')

    ctx.deploy = ctx.sdk_client_rpc.get_deploy(ctx.deploy_result.hash)
    assert ctx.deploy

    args = ctx.deploy['deploy']['session']['Transfer']['args']
    assert args

    for arg in range(len(args)):
        if args[arg][0] == 'MAP':
            ctx.CLV_map = args[arg][1]

    assert ctx.CLV_map


@step('the map\'s key is "(.*)" and value is "(.*)"')
def map_has_kay_and_value(ctx, key, value):
    print(f'the map\'s key is "{key}" and value is "{value}"')

    """
    The SDK doesn't decode the deploys CLV_Type
    We can not retrieve it's values here
    (The node will return 'parsed' values for simple CLV_Types only)
    """

    assert False


@given('a nested map is created \{"(.*)": \{"(.*)": (.*)\}, "(.*)": \{"(.*)", (.*)\}\}')
def nested_map_is_created(ctx, key0, key1, value1, key2, key3, value2):
    print(f'a nested map is created "{key0}": "{key1}": {value1}, "{key2}": "{key3}", {value2}')

    _list1 = []
    _tuple: typing.Tuple = (CLV_String(key1), CLV_U32(int(value1)))
    _list1.append(_tuple)

    _list2 = []
    _tuple: typing.Tuple = (CLV_String(key3), CLV_U32(int(value2)))
    _list2.append(_tuple)

    _rootMap = []
    _tuple1: typing.Tuple = (CLV_String(key0), CLV_Map(_list1))
    _tuple2: typing.Tuple = (CLV_String(key2), CLV_Map(_list2))

    _rootMap.append(_tuple1)
    _rootMap.append(_tuple2)

    ctx.CLV_map = CLV_Map(_rootMap)

    assert ctx.CLV_map


@step('the 1st nested map\'s key is "(.*)" and value is "(.*)"')
def the_nth_key_and_value_are(ctx, key, value):
    print(f'the 1st nested map\'s key is "{key}" and value is "{value}"')

    """
    The SDK doesn't decode the deploys CLV_Type
    We can not retrieve it's values here
    (The node will return 'parsed' values for simple CLV_Types only)
    """

    assert False


@step('the map\'s bytes are "(.*)"')
def the_maps_bytes_are(ctx, hex_bytes):
    print(f'the map\'s bytes are "{hex_bytes}"')

    assert ctx.CLV_map['bytes'] == hex_bytes


@given(
    'a nested map is created  \{(.*): \{(.*): \{(.*): "(.*)"\}, (.*): \{(.*): "(.*)"\}\}, (.*): \{(.*): \{(.*): "(.*)"\}, (.*): \{(.*): "(.*)"\}\}\}')
def a_nested_map_is_created(ctx, key1, key11, key111, value111, key12, key121, value121, key2, key21, key211, value211, key22, key221, value221):
    print(f'a nested map is created  {key1}: {key11}: {key111}: "{value111}", {key12}: {key121}: "{value121}", {key2}: {key21}: {key211}: "{value211}", {key22}: {key221}: "{value221}"')

    # TODO
    # The below fails to give the expected bytes
    # Need to ascertain that the bytes expected are actually correct

    _list111 = []
    _tuple: typing.Tuple = (CLV_U256(int(key111)), CLV_String(value111))
    _list111.append(_tuple)

    _list121 = []
    _tuple: typing.Tuple = (CLV_U32(int(key121)), CLV_String(value121))
    _list121.append(_tuple)

    _list11 = []
    _tuple1: typing.Tuple = (CLV_U256(int(key11)), CLV_Map(_list111))
    _tuple2: typing.Tuple = (CLV_U256(int(key12)), CLV_Map(_list121))
    _list11.append(_tuple1)
    _list11.append(_tuple2)

    _list211 = []
    _tuple: typing.Tuple = (CLV_U256(int(key211)), CLV_String(value211))
    _list211.append(_tuple)

    _list221 = []
    _tuple: typing.Tuple = (CLV_U32(int(key221)), CLV_String(value221))
    _list221.append(_tuple)

    _list21 = []
    _tuple1: typing.Tuple = (CLV_U256(int(key11)), CLV_Map(_list211))
    _tuple2: typing.Tuple = (CLV_U256(int(key12)), CLV_Map(_list221))
    _list21.append(_tuple1)
    _list21.append(_tuple2)

    _rootMap = []
    _tuple1: typing.Tuple = (CLV_U256(int(key1)), CLV_Map(_list11))
    _tuple2: typing.Tuple = (CLV_U256(int(key2)), CLV_Map(_list21))

    _rootMap.append(_tuple1)
    _rootMap.append(_tuple2)

    ctx.CLV_map = CLV_Map(_rootMap)

    assert ctx.CLV_map


@step('the map\'s key type is "(.*)" and the maps value type is "(.*)"')
def step_impl(ctx, key1, key2):
    map_has_value(ctx, key1, key2)


def deploy_map(ctx):

    ctx.user_1 = '1'
    ctx.user_2 = '2'
    ctx.transfer_amount = 2500000000
    ctx.gas_price = 1
    ctx.ttl = '30m'
    ctx.payment_amount = 100000000

    ctx.CLV_values = []
    ctx.CLV_values.append({'MAP': ctx.CLV_map})

    ctx.CLV_map = ""

    deploy_set_signatures(ctx)

    ctx.deploy = create_deploy(ctx)

    ctx.sdk_client_rpc.send_deploy(ctx.deploy)
    ctx.deploy_result = ctx.deploy

    assert ctx.deploy_result.hash.hex()

