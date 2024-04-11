from behave import *
from pycspr import types

from test.features.steps.utils.asyncs import call_async_function, deploy_event
from test.features.steps.utils.deploy import deploy_set_signatures, create_deploy, deploy_to_chain

use_step_matcher("re")


@given('an Any value contains a byte array value of "(.*)"')
def step_impl(ctx, _bytes):
    print(f'an Any value contains a byte array value of "{_bytes}"')

    ctx.any_type = types.CL_Any(str.encode(_bytes))
    assert ctx.any_type


@then('the any value\'s bytes are "(.*)"')
def step_impl(ctx, _bytes):
    print(f'he any value\'s bytes are "{_bytes}"')

    any_type: types.CL_Any = ctx.any_type
    assert any_type.value == str.encode(_bytes)


@given("that the any value is deployed in a transfer as a named argument")
def step_impl(ctx):
    print(f'that the any value is deployed in a transfer as a named argument')

    ctx.user_1 = '1'
    ctx.user_2 = '2'
    ctx.transfer_amount = 2500000000
    ctx.gas_price = 1
    ctx.ttl = '30m'
    ctx.payment_amount = 100000000
    ctx.cl_values.append({"ANY": ctx.any_type})

    deploy_set_signatures(ctx)

    # Will fail here
    # Decode of ANY value not implemented in the SDK yet in
    # serialisation/binary/cl_value/decoder.py:32

    ctx.deploy = create_deploy(ctx)

    ctx.deploy_result = deploy_to_chain(ctx)

    assert ctx.deploy


@step("the transfer containing the any value is successfully executed")
def step_impl(ctx):
    print(f'the transfer containing the any value is successfully executed')

    ctx.timeout = 300
    ctx.deploy.hash = ctx.deploy_result.hash
    ctx.execution_result = call_async_function(ctx, deploy_event)

    assert ctx.execution_result[0]['result']['Success']


@when("the any is read from the deploy")
def step_impl(ctx):
    print(f'the any is read from the deploy')

    ctx.deploy = ctx.sdk_client_rpc.get_deploy(ctx.deploy_result.hash)
    assert ctx.deploy

    args = ctx.deploy.session.args
    assert args

    _read = False
    for arg in range(len(args)):
        if args[arg].name == "ANY":
            ctx.any_type = types.CL_Any(args[arg].value['bytes'])
            assert ctx.any_type
            _read = True

    assert _read


@given('that the map of public keys to any types is read from resource "(.*)"')
def step_impl(ctx, _resource):
    print(f'that the map of public keys to any types is read from resource "{_resource}"')
    raise NotImplementedError('step not implemented')


@then("the loaded CLMap will contain 0 elements as nested any values are not supported")
def step_impl(ctx):
    print(f'the loaded CLMap will contain 0 elements as nested any values are not supported')
    raise NotImplementedError('step not implemented')


@step('the nested map key type will be "(.*)"')
def step_impl(ctx, _type):
    print(f'the nested map key type will be "{_type}"')
    raise NotImplementedError('step not implemented')


@step('the nested map value type will be "(.*)"')
def step_impl(ctx, _type):
    print(f'the nested map value type will be "{_type}"')
    raise NotImplementedError('step not implemented')


@step('the maps bytes will be "(.*)"')
def step_impl(ctx, _bytes):
    print(f'the maps bytes will be "{_bytes}"')
    raise NotImplementedError('step not implemented')

