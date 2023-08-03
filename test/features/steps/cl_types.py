from behave import *

from test.features.steps.utils.asyncs import deploy_event, call_async_function
from test.features.steps.utils.cl_types_factory import CLTypesFactory
from test.features.steps.utils.deploy import deploy_set_signatures, create_deploy

use_step_matcher("re")

# Step Definitions for CL Types Cucumber Tests

_factory = CLTypesFactory()


@given('that a CL value of type "(.*)" has a value of "(.*)"')
def that_a_cl_value_of_type_hash_vale(ctx, _type, _value):
    print(f'that a CL value of type "{_type}" has a value of "{_value}"')

    ctx.cl_values.append({'hex_bytes': _factory.create_value(_type, _value, ctx)})


@then('it\'s bytes will be "(.*)"')
def bytes_will_be(ctx, hex_bytes):
    print(f'it\'s bytes will be "{hex_bytes}"')

    assert ctx.cl_values[-1]['hex_bytes'] == hex_bytes


@given('that the CL complex value of type "(.*)" with an internal types of "(.*)" values of "(.*)"')
def the_complex_type_with_internal_type_has_value(ctx, type_complex, type_internal, _value):
    print(
        f'that the CL complex value of type "{type_complex}" with an internal types of "{type_internal}" values of "{_value}"')

    ctx.cl_values.append({'hex_bytes': _factory.create_complex_value(type_complex, type_internal.split(','), _value.split(','), ctx)})


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
            assert_value(args[arg][1], _value)
            assert_bytes(args[arg][1], _bytes)
            compared = True

    assert compared


@step(
    'the deploys NamedArgument Complex value "(.*)" has internal types of "(.*)" and values of "(.*)" and bytes of "(.*)"')
def named_argument_has_values(ctx, _complex, internal, _value, _bytes):
    print(
        f'the deploys NamedArgument Complex value "{_complex}" has internal types of "{internal}" and values of "{_value}" and bytes of "{_bytes}"')

    args = ctx.deploy['deploy']['session']['Transfer']['args']
    assert args

    _internals: list = internal.split(',')
    _values: list = _value.split(',')

    compared = False
    for arg in range(len(args)):
        if args[arg][0] == _complex:
            if _complex == 'Map':
                assert_map(_values, args[arg][1], _bytes)
                compared = True
            elif _complex == 'Option':
                assert_option(_internals, args[arg][1], _bytes)
                compared = True
            elif _complex == 'List':
                assert_list(_internals, args[arg][1], _bytes, _values)
                compared = True
            elif _complex in ['Tuple1', 'Tuple2', 'Tuple3']:
                assert_tuple(_internals, _complex, args, arg, _bytes, _values)
                compared = True
            else:
                raise ValueError(f'Unknown CL type: {_complex}')

    assert compared


def assert_map(_values, args, _bytes):
    assert args['bytes'] == _bytes
    for i in range(len(_values)):
        assert _values[i] == args['parsed'][i]['value']


def assert_option(_internals, args, _bytes):
    assert args['cl_type']['Option'] == _internals[0]
    assert args['bytes'] == _bytes


def assert_list(_internals, args, _bytes, _values):
    assert args['bytes'] == _bytes
    assert args['parsed'] == _values


def assert_tuple(_internals, _complex, args, arg, _bytes, _values):
    assert args[arg][1]['bytes'] == _bytes
    for i in range(len(_values)):
        assert args[arg][1]['cl_type'][_complex][i] == _internals[i]
        assert str(args[arg][1]['parsed'][i]).lower() == _values[i].lower()


def assert_value(arg, _value):
    if arg['cl_type'] == 'Key':
        return True
    elif arg['cl_type'] == 'URef':
        assert arg['parsed'][5:-4] == _value
    else:
        assert str(arg['parsed']).lower() == str(_value).lower()


def assert_bytes(arg, value):
    if arg['cl_type'] == 'Key':
        assert str(arg['bytes'])[2:] == str(value)
    else:
        assert str(arg['bytes']) == str(value)
