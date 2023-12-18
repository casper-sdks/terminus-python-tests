from behave import *

use_step_matcher("re")


@given('an Any value contains a "(.*)" value of "(.*)"')
def contains_type_and_value(ctx, cltype, val):
    print(f'an Any value contains a {cltype} value of {val}')


@then('the any value\'s bytes are "(.*)"')
def its_bytes_are(ctx, hex_bytes):
    print(f'the any value\'s bytes are "{hex_bytes}"')


@given("that the any value is deployed in a transfer as a named argument")
def is_deployed(ctx):
    print(f'that the any value is deployed in a transfer as a named argument')


@step("the transfer containing the any value is successfully executed")
def deploy_successful(ctx):
    print(f'the transfer containing the any value is successfully executed')


@when("the any is read from the deploy")
def read_from_the_deploy(ctx):
    print(f'the any is read from the deploy')


@step('the type of the any is "Bool" with a value of "true"')
def bool_type_is_true(ctx):
    print(f'the type of the any is "Bool" with a value of "true"')
