from behave import *

use_step_matcher("re")


@given('a list is created with "(.*)" values of \("(.*)", "(.*)", "(.*)"\)')
def list_is_created(ctx, cl_type, val1, val2, val3):
    print(f'a list is created with "{cl_type}" values of \("{val1}", "{val2}", "{val3}"\)')


@then('the list\'s bytes are "(.*)"')
def its_bytes_are(ctx, hex_bytes):
    print(f'the list\'s bytes are "{hex_bytes}')


@step("the list's length is (.*)")
def its_length_is(ctx, _length):
    print(f"the list's length is {_length}")


@step('the list\'s "(.*)" item is a CLValue with "(.*)" value of "(.*)"')
def list_string_item_is(ctx, nth, cl_type, value):
    print(f'the list\'s "{nth}" item is a CLValue with "{cl_type}" value of "{value}"')


@given("that the list is deployed in a transfer")
def it_is_deployed(ctx):
    print(f'that the list is deployed in a transfer')


@step("the transfer containing the list is successfully executed")
def it_is_successful(ctx):
    print(f'the transfer containing the list is successfully executed')


@when("the list is read from the deploy")
def it_is_read_from_the_deploy(ctx):
    print(f'the list is read from the deploy')


@given("a list is created with (.*) values of \((.*), (.*), (.*)\)")
def another_list_is_created(ctx, cl_type, val1, val2, val3):
    print(f'a list is created with "{cl_type}" values of \({val1}, {val2}, {val3}\)')


@step('the list\'s "(.*)" item is a CLValue with (.*) value of (.*)')
def list_number_item_is(ctx, nth, cl_type, value):
    print(f'the list\'s "{nth}" item is a CLValue with "{cl_type}" value of "{value}"')


@given("a nested list is created with (.*) values of \(\((.*), (.*), (.*)\),\((.*), (.*), (.*)\)\)")
def a_complex_nested_list_is_created(ctx, cl_type, val1, val2, val3, val4, val5, val6):
    print(f'a nested list is created with {cl_type} values of \(\({val1}, {val2}, {val3}\),\({val4}, {val5}, {val6}\)\)')


@step('the "(.*)" nested list\'s "(.*)" item is a CLValue with (.*) value of (.*)')
def complex_list_has_values(ctx, nth1, nth2, cl_type, value):
    print(f'the "{nth1}" nested list\'s "{nth2}" item is a CLValue with {cl_type} value of {value}')
