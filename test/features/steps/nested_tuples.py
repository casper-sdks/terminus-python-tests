from behave import *

use_step_matcher("re")


@given("that a nested Tuple1 is defined as \(\((.*)\) using U32 numeric values")
def nested_tuple1(ctx, value):
    print(f'that a nested Tuple1 is defined as \(\({value}\) using U32 numeric values')


@given("that a nested Tuple2 is defined as \((.*), \((.*), \((.*), (.*)\)\)\) using U32 numeric values")
def nested_tuple2(ctx, arg0, arg1, arg2, arg3):
    print(f'that a nested Tuple2 is defined as \({arg0}, \({arg1}, \({arg2}, {arg3}\)\)\) using U32 numeric values"')


@then('the "(.*)" element of the Tuple(.*) is (.*)')
def element_is_equal(ctx, index, _tuple, expected):
    print(f'the "{index}" element of the Tuple{_tuple} is {expected}')


@step('the Tuple(.*) bytes are "(.*)"')
def tuple_bytes(ctx, _tuple, _bytes):
    print(f'the Tuple{_tuple} bytes are "{_bytes}"')


@given("that a nested Tuple3 is defined as \((.*), (.*), \((.*), (.*), \((.*), (.*), (.*)\)\)\) using U32 numeric values")
def nested_tuple3(ctx, arg0, arg1, arg2, arg3, arg4, arg5, arg6):
    print(f'that a nested Tuple3 is defined as \({arg0}, {arg1}, \({arg2}, {arg3}, \({arg4}, {arg5}, {arg6}\)\)\) using U32 numeric values')


@given("that the nested tuples are deployed in a transfer")
def deployed(ctx):
    print(f'that the nested tuples are deployed in a transfer')


@step("the transfer is successful")
def deploy_successful(ctx):
    print(f'the transfer is successful')


@when("the tuples deploy is obtained from the node")
def tuples_obtained(ctx):
    print(f'the tuples deploy is obtained from the node')


