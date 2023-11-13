from behave import *

use_step_matcher("re")


@given('a map is created \{"(.*)": (.*)\}')
def a_map_is_created(context, key, value):
    print(f'a map is created {key}:{value}')



@then('the map\'s key type is "(.*)" and the maps value type is "(.*)"')
def map_has_value(context, key, value):
    print(f'the map\'s key type is "{key}" and the maps value type is "{value}"')


@then('the map\'s bytes are "(.*)"')
def map_has_bytes(context, hexBytes):
    print(f'the map\'s bytes are "{hexBytes}"')


@given("that the nested map is deployed in a transfer")
def map_is_deployed(context):
    print(f'that the nested map is deployed in a transfer')


@step("the transfer containing the nested map is successfully executed")
def map_is_deployed_successfully(context):
    print(f'the transfer containing the nested map is successfully executed')


@when("the map is read from the deploy")
def map_is_read_from_the_deploy(context):
    print(f'the map is read from the deploy')


@step('the map\'s key is "(.*)" and value is "(.*)"')
def map_has_kay_and_value(context, key, value):
    print(f'the map\'s key is "{key}" and value is "{value}"')


@given('a nested map is created \{"(.*)": \{"(.*)": (.*)\}, "(.*)": \{"(.*)", (.*)\}\}')
def nested_map_is_created(context, key1, key2, value1, key4, key5, value2):
    print(f'a nested map is created "{key1}": "{key2}": {value1}, "{key4}": "{key5}", {value2}')


@step('the 1st nested map\'s key is "(.*)" and value is "(.*)"')
def the_nth_key_and_value_are(context, key, value):
    print(f'the 1st nested map\'s key is "{key}" and value is "{value}"')

@given(
    'a nested map is created  \{1: \{11: \{111: "ONE_ONE_ONE"\}, 12: \{121: "ONE_TWO_ONE"\}\}, 2: \{21: \{211: "TWO_ONE_ONE"\}, 22: \{221: "TWO_TWO_ONE"\}\}\}')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(
        u'STEP: Given a nested map is created  {1: {11: {111: "ONE_ONE_ONE"}, 12: {121: "ONE_TWO_ONE"}}, 2: {21: {211: "TWO_ONE_ONE"}, 22: {221: "TWO_TWO_ONE"}}}')


@step('the map\'s bytes are "(.*)"')
def step_impl(context, hexBytes):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And the map\'s bytes are "01000000030000004f4e4502000000"')
