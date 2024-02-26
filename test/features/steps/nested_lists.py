from behave import *
from pycspr import types, serialisation

from test.features.steps.utils.asyncs import call_async_function, deploy_event
from test.features.steps.utils.cl_types_factory import CLTypesFactory
from test.features.steps.utils.cl_utils import CLTypesUtils
from test.features.steps.utils.deploy import deploy_set_signatures, create_deploy

use_step_matcher("re")

_factory = CLTypesFactory()
_utils = CLTypesUtils()

# Step Definitions for Nested Lists CL Types Cucumber Tests


@given('a list is created with "(.*)" values of \("(.*)", "(.*)", "(.*)"\)')
def list_is_created(ctx, cl_type, val1, val2, val3):
    print(f'a list is created with "{cl_type}" values of \("{val1}", "{val2}", "{val3}"\)')

    _list = [_factory.create_value(cl_type, val1),
             _factory.create_value(cl_type, val2),
             _factory.create_value(cl_type, val3)]

    ctx.cl_list = types.CL_List(_list)

    assert ctx.cl_list


@then('the list\'s bytes are "(.*)"')
def its_bytes_are(ctx, hex_bytes):
    print(f'the list\'s bytes are "{hex_bytes}')

    """
    The test will fail here when checking the CL_Type from the Deploy
    The CL_Type needs to be serialised into a CL_Type object
    """

    assert serialisation.to_bytes(ctx.cl_list).hex() == hex_bytes


@step("the list's length is (.*)")
def its_length_is(ctx, _length):
    print(f"the list's length is {_length}")

    """
    The test will fail here when checking the CL_Type from the Deploy
    The CL_Type needs to be serialised into a CL_Type object
    """

    assert len(ctx.cl_list.vector) == int(_length)


@step('the list\'s "(.*)" item is a CLValue with "(.*)" value of "(.*)"')
def list_string_item_is(ctx, nth, cl_type, value):
    print(f'the list\'s "{nth}" item is a CLValue with "{cl_type}" value of "{value}"')

    """
    The test will fail here when checking the CL_Type from the Deploy
    The CL_Type needs to be serialised into a CL_Type object
    """

    _item = ctx.cl_list.vector[(int(nth[0])) - 1]
    assert str(_item.value).lower() == value.lower()
    assert isinstance(_item, _utils.cl_values_map[cl_type])


@given("that the list is deployed in a transfer")
def it_is_deployed(ctx):
    print(f'that the list is deployed in a transfer')

    deploy_list(ctx)


@step("the transfer containing the list is successfully executed")
def it_is_successful(ctx):
    print(f'the transfer containing the list is successfully executed')

    ctx.timeout = 300
    ctx.execution_result = call_async_function(ctx, deploy_event)
    assert ctx.execution_result[0]['result']['Success']


@when("the list is read from the deploy")
def it_is_read_from_the_deploy(ctx):
    print(f'the list is read from the deploy')

    ctx.deploy = ctx.sdk_client.get_deploy(ctx.deploy_result.hash)
    assert ctx.deploy

    args = ctx.deploy['deploy']['session']['Transfer']['args']
    assert args

    for arg in range(len(args)):
        if args[arg][0] == 'LIST':
            ctx.cl_list = args[arg][1]

    assert ctx.cl_list


@given("a list is created with (.*) values of \((.*), (.*), (.*)\)")
def another_list_is_created(ctx, cl_type, val1, val2, val3):
    print(f'a list is created with "{cl_type}" values of \({val1}, {val2}, {val3}\)')

    _list = [_factory.create_value(cl_type, int(val1)),
             _factory.create_value(cl_type, int(val2)),
             _factory.create_value(cl_type, int(val3))]

    ctx.cl_list = types.CL_List(_list)

    assert ctx.cl_list


@step('the list\'s "(.*)" item is a CLValue with (.*) value of (.*)')
def list_number_item_is(ctx, nth, cl_type, value):
    print(f'the list\'s "{nth}" item is a CLValue with "{cl_type}" value of "{value}"')

    """
    The test will fail here when checking the CL_Type from the Deploy
    The CL_Type needs to be serialised into a CL_Type object
    """

    _item = ctx.cl_list.vector[(int(nth[0])) - 1]
    assert str(_item.value).lower() == value.lower()
    assert isinstance(_item, _utils.cl_values_map[cl_type])


@given("a nested list is created with (.*) values of \(\((.*), (.*), (.*)\),\((.*), (.*), (.*)\)\)")
def a_complex_nested_list_is_created(ctx, cl_type, val1, val2, val3, val4, val5, val6):
    print(
        f'a nested list is created with {cl_type} values of \(\({val1}, {val2}, {val3}\),\({val4}, {val5}, {val6}\)\)')

    """
    The below fails to build correctly
    The bytes check fails
    The SDK _encode function doesn't look for nested values
    """

    _list = [[_factory.create_value(cl_type, int(val1)),
              _factory.create_value(cl_type, int(val2)),
              _factory.create_value(cl_type, int(val3))],
             [_factory.create_value(cl_type, int(val4)),
              _factory.create_value(cl_type, int(val5)),
              _factory.create_value(cl_type, int(val6))]
             ]

    ctx.cl_list = types.CL_List(_list)

    assert ctx.cl_list


@step('the "(.*)" nested list\'s "(.*)" item is a CLValue with (.*) value of (.*)')
def complex_list_has_values(ctx, nth1, nth2, cl_type, value):
    print(f'the "{nth1}" nested list\'s "{nth2}" item is a CLValue with {cl_type} value of {value}')

    """
    The test will fail here when checking the CL_Type from the Deploy
    The CL_Type needs to be serialised into a CL_Type object
    """
    _item = ctx.cl_list.vector[(int(nth1[0])) - 1][(int(nth2[0])) - 1]
    assert str(_item.value).lower() == value.lower()
    assert isinstance(_item, _utils.cl_values_map[cl_type])


def deploy_list(ctx):
    ctx.user_1 = '1'
    ctx.user_2 = '2'
    ctx.transfer_amount = 2500000000
    ctx.gas_price = 1
    ctx.ttl = '30m'
    ctx.payment_amount = 100000000

    ctx.cl_values = []
    ctx.cl_values.append({'LIST': ctx.cl_list})

    ctx.cl_list = ""

    deploy_set_signatures(ctx)

    ctx.deploy = create_deploy(ctx)

    ctx.sdk_client.send_deploy(ctx.deploy)
    ctx.deploy_result = ctx.deploy

    assert ctx.deploy_result.hash.hex()
