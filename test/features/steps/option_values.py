from behave import *

use_step_matcher("re")


@given("that an Option value has an empty value")
def has_empty_value(ctx):
    print(f'that an Option value has an empty value')


@then("the Option value is not present")
def no_value_present(ctx):
    print(f'the Option value is not present')


@step('the Option value\'s bytes are (.*)')
def bytes_are(ctx, hex_bytes):
    print(f'the Option value\'s bytes are {hex_bytes}')


@given('an Option value contains a "(.*)" value of "(.*)"')
def contains_type_value(ctx, _type, _value):
    print(f'an Option value contains a "{_type}" value of "{_value}"')


@given("that the Option value is deployed in a transfer as a named argument")
def is_deployed(ctx):
    print(f'that the Option value is deployed in a transfer as a named argument')


@step("the transfer containing the Option value is successfully executed")
def is_successful(ctx):
    print(f'the transfer containing the Option value is successfully executed')


@when("the Option is read from the deploy")
def is_read(ctx):
    print(f'the Option is read from the deploy')


@step('the type of the Option is "(.*)" with a value of "(.*)"')
def has_type_of(ctx, _type, _value):
    print(f'the type of the Option is "{_type}" with a value of "{_value}"')
