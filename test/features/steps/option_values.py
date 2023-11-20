from behave import *
from pycspr import types, serialisation

from test.features.steps.utils.asyncs import call_async_function, deploy_event
from test.features.steps.utils.cl_types_factory import CLTypesFactory
from test.features.steps.utils.cl_utils import CLTypesUtils
from test.features.steps.utils.deploy import deploy_set_signatures, create_deploy

use_step_matcher("re")

_factory = CLTypesFactory()
_utils = CLTypesUtils()

# Step Definitions for CL Type Option Cucumber Tests


@given("that an Option value has an empty value")
def has_empty_value(ctx):
    print(f'that an Option value has an empty value')

    ctx.cl_option = types.CL_Option(None, None)


@then("the Option value is not present")
def no_value_present(ctx):
    print(f'the Option value is not present')

    assert ctx.cl_option.option_type is None
    assert ctx.cl_option.value is None


@step('the Option value\'s bytes are (.*)')
def bytes_are(ctx, hex_bytes):
    print(f'the Option value\'s bytes are {hex_bytes}')

    """
    The test will fail here when checking the CL_Type from the Deploy
    The CL_Type needs to be serialised into a CL_Type object
    """

    """
    The test will also fail here when checking the bytes of CL_Any
    The bytes encoder throws NotImplementedError 
    """

    if hex_bytes == '""':
        hex_bytes = '00'

    assert serialisation.to_bytes(ctx.cl_option).hex() == hex_bytes.replace('"', '')


@given('an Option value contains a "(.*)" value of "(.*)"')
def contains_type_value(ctx, _type, _value):
    print(f'an Option value contains a "{_type}" value of "{_value}"')

    ctx.cl_option = types.CL_Option(_factory.create_value(_type, _value),
                                    _utils.cl_types_map['CL_' + _type])

    assert ctx.cl_option


@given("that the Option value is deployed in a transfer as a named argument")
def is_deployed(ctx):
    print(f'that the Option value is deployed in a transfer as a named argument')

    deploy_option(ctx)


@step("the transfer containing the Option value is successfully executed")
def is_successful(ctx):
    print(f'the transfer containing the Option value is successfully executed')

    ctx.timeout = 300
    ctx.execution_result = call_async_function(ctx, deploy_event)
    assert ctx.execution_result[0]['result']['Success']


@when("the Option is read from the deploy")
def is_read(ctx):
    print(f'the Option is read from the deploy')

    ctx.deploy = ctx.sdk_client.get_deploy(ctx.deploy_result.hash)

    assert ctx.deploy

    args = ctx.deploy['deploy']['session']['Transfer']['args']
    assert args

    for arg in range(len(args)):
        if args[arg][0] == 'OPTION':
            ctx.cl_option = args[arg][1]

    assert ctx.cl_option


@step('the type of the Option is "(.*)" with a value of "(.*)"')
def has_type_of(ctx, _type, _value):
    print(f'the type of the Option is "{_type}" with a value of "{_value}"')


def deploy_option(ctx):

    """
    The test will fail here when setting OPTION of type CL_ByteArray
    CL_ByteArray is not being set correctly as an option
    """

    ctx.user_1 = '1'
    ctx.user_2 = '2'
    ctx.transfer_amount = 2500000000
    ctx.gas_price = 1
    ctx.ttl = '30m'
    ctx.chain = 'casper-net-1'
    ctx.payment_amount = 100000000

    ctx.cl_values = []
    ctx.cl_values.append({'OPTION': ctx.cl_option})

    ctx.cl_option = ""

    deploy_set_signatures(ctx)

    ctx.deploy = create_deploy(ctx)

    ctx.sdk_client.send_deploy(ctx.deploy)
    ctx.deploy_result = ctx.deploy

    assert ctx.deploy_result.hash.hex()
