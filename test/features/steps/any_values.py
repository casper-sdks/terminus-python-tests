from behave import *

from test.features.steps.utils.cl_types_factory import CLTypesFactory
from test.features.steps.utils.cl_utils import CLTypesUtils

use_step_matcher("re")

_factory = CLTypesFactory()
_utils = CLTypesUtils()


@given('an Any value contains a "(.*)" value of "(.*)"')
def contains_type_and_value(ctx, cltype, val):
    print(f'an Any value contains a {cltype} value of {val}')

    _bytes = _factory.create_value(cltype, val)
    ctx.cl_any = _factory.create_value('Any', _bytes.value.hex())

    assert ctx.cl_any
    assert ctx.cl_any.value.hex() == val

@then('the any value\'s bytes are "(.*)"')
def its_bytes_are(ctx, hex_bytes):
    assert ctx.cl_any.value.hex() == hex_bytes


@given("that the any value is deployed in a transfer as a named argument")
def is_deployed(ctx):
    print(f'that the any value is deployed in a transfer as a named argument')





@step("the transfer containing the any value is successfully executed")
def deploy_successful(ctx):
    print(f'the transfer containing the any value is successfully executed')


@when("the any is read from the deploy")
def read_from_the_deploy(ctx):
    print(f'the any is read from the deploy')


@given('that the map of public keys to any types is read from resource "(.*)"')
def resource_is_read(ctx, resource):
    print(f'that the map of public keys to any types is read from resource "{resource}"')


@then("the loaded CLMap will contain 1 elements")
def loaded_map_is(ctx):
    print(f'the loaded CLMap will contain 1 elements')


@step('the nested map key type will be "(.*)"')
def nested_map_key_is(ctx, cltype):
    print(f'the nested map key type will be "{cltype}"')


@step('the nested map value type will be "(.*)"')
def nested_map_value_is(ctx, cltype):
    print(f'the nested map value type will be "{cltype}"')


@step(
    'the maps bytes will be "(.*)"')
def the_map_bytes_are(ctx, hex_bytes):
    print(f'the nested map value type will be "{hex_bytes}"')


@step('the nested map keys value will be "(.*)"')
def the_nested_map_keys_value_is(ctx, val):
    print(f'the nested map keys value will be "{val}"')


@step("the nested map any values bytes length will by (.*)")
def the_nested_map_any_bytes_length_is(ctx, len):
    print(f'the nested map any values bytes length will by {len}')


@step('the nested map any values bytes will by "(.*)"')
def the_nested_map_value_bytes_are(ctx, hex_bytes):
    print(f'the nested map any values bytes will by {hex_bytes}')
