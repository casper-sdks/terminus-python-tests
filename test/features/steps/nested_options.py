from behave import *

from test.features.steps.utils.cl_types_factory import CLTypesFactory
from test.features.steps.utils.cl_utils import CLTypesUtils

use_step_matcher("re")

_factory = CLTypesFactory()
_utils = CLTypesUtils()


# Step Definitions for Nested CL Type Option Cucumber Tests

@given(
    'that a nested Option has an inner type of (.*) with a type of (.*) and a value of "(.*)"')
def nested_option_created(ctx, _type, _type_inner, _value):
    print(f'that a nested Option has an inner type of {_type} with a type of {_type_inner} and a value of "{_value}"')


@then('the inner type is (.*) with a type of (.*) and a value of "(.*)"')
def nested_option_has_values(ctx, _type, _type_inner, _value):
    print(f'the inner type is {_type} with a type of {_type_inner} and a value of "{_value}"')


@step('the bytes are "(.*)"')
def bytes_are(ctx, hex_bytes):
    print(f'the bytes are "{hex_bytes}"')


@given("that the nested Option is deployed in a transfer")
def is_deployed(ctx):
    print(f'that the nested Option is deployed in a transfer')


@step("the transfer containing the nested Option is successfully executed")
def step_impl(ctx):
    print(f'the transfer containing the nested Option is successfully executed')
