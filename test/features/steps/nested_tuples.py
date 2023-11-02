from behave import *
from pycspr import types, serialisation

use_step_matcher("re")


@given("that a nested Tuple1 is defined as \((.*)\) using U32 numeric values")
def nested_tuple1(ctx, value):
    print(f'that a nested Tuple1 is defined as \(\({value}\) using U32 numeric values')

    ctx.tuple_root_1 = types.CL_Tuple1(types.CL_Tuple1(types.CL_U32(value)))


@given("that a nested Tuple2 is defined as \((.*), \((.*), \((.*), (.*)\)\)\) using U32 numeric values")
def nested_tuple2(ctx, arg0, arg1, arg2, arg3):
    print(f'that a nested Tuple2 is defined as \({arg0}, \({arg1}, \({arg2}, {arg3}\)\)\) using U32 numeric values"')

    ctx.tuple_root_2 = types.CL_Tuple2(
        types.CL_U32(int(arg0)),
        types.CL_Tuple2(
            types.CL_U32(int(arg1)),
            types.CL_Tuple2(
                types.CL_U32(int(arg2)),
                types.CL_U32(int(arg3))
            )
        )
    )

    assert ctx.tuple_root_2


@then('the "(.*)" element of the Tuple(.*) is (.*)')
def element_is_equal(ctx, index, _tuple, expected):
    print(f'the "{index}" element of the Tuple{_tuple} is {expected}')

    expected_list = expected.replace('"', '').replace("(", "").replace(")", "").split(",")
    _expected = [int(i.strip()) for i in expected_list]

    cl_type = get_tuple_value(int(_tuple), index, ctx)

    assert cl_type == _expected


@step('the Tuple(.*) bytes are "(.*)"')
def tuple_bytes(ctx, _tuple, _bytes):
    print(f'the Tuple{_tuple} bytes are "{_bytes}"')

    _bytes_tuple = ''

    if _tuple == '1':
        _bytes_tuple = ctx.tuple_root_1
    if _tuple == '2':
        _bytes_tuple = ctx.tuple_root_2
    if _tuple == '3':
        _bytes_tuple = ctx.tuple_root_3

    assert serialisation.to_bytes(_bytes_tuple).hex() == _bytes


@given("that a nested Tuple3 is defined as \((.*), (.*), \((.*), (.*), \((.*), (.*), (.*)\)\)\) using U32 numeric values")
def nested_tuple3(ctx, arg0, arg1, arg2, arg3, arg4, arg5, arg6):
    print(f'that a nested Tuple3 is defined as \({arg0}, {arg1}, \({arg2}, {arg3}, \({arg4}, {arg5}, {arg6}\)\)\) using U32 numeric values')

    ctx.tuple_root_3 = types.CL_Tuple3(
        types.CL_U32(int(arg0)),
        types.CL_U32(int(arg1)),
        types.CL_Tuple3(
            types.CL_U32(int(arg2)),
            types.CL_U32(int(arg3)),
            types.CL_Tuple3(
                types.CL_U32(int(arg4)),
                types.CL_U32(int(arg5)),
                types.CL_U32(int(arg6))
            )
        )
    )

    assert ctx.tuple_root_3



@given("that the nested tuples are deployed in a transfer")
def deployed(ctx):
    print(f'that the nested tuples are deployed in a transfer')


@step("the transfer is successful")
def deploy_successful(ctx):
    print(f'the transfer is successful')


@when("the tuples deploy is obtained from the node")
def tuples_obtained(ctx):
    print(f'the tuples deploy is obtained from the node')


def get_tuple_value(_tuple, index, ctx):

    if _tuple == 1:
        return ctx.tuple_root_1.v0
    if _tuple == 2:
        return get_tuple_tree_value(_tuple, ctx.tuple_root_2, index)
    if _tuple == 3:
        return get_tuple_tree_value(_tuple, ctx.tuple_root_3, index)


def get_tuple_tree_value(_tuple, cltype, index):

    ret = []

    _methods = [attr for attr in dir(cltype) if attr.startswith('v')]

    if index == 'first':
        ret.append(cltype.v0.value)
        return ret
    else:
        if index == 'second':
            func = cltype.v1
        else:
            func = cltype.v2
        _methods = ['func.' + attr for attr in dir(func) if attr.startswith('v')]
        for _method in _methods:
            if 'value' in _method:
                ret.append(eval(_method))
            else:
                ret = (iterate_type(eval(_method), ret))
        return ret


def iterate_type(func, ret) -> list:
    if hasattr(func, 'value'):
        ret.append(func.value)
    else:
        _methods = ['func.' + attr for attr in dir(func) if attr.startswith('v')]
        for _method in _methods:
            iterate_type(eval(_method), ret)

    return ret
