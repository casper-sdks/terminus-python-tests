from behave import *
from pycspr import types, serialisation

from test.features.steps.utils.asyncs import call_async_function, deploy_event
from test.features.steps.utils.deploy import deploy_set_signatures, create_deploy

use_step_matcher("re")


# Step Definitions for Nested Tuple CL Types Cucumber Tests


@given("that a nested Tuple1 is defined as \((.*)\) using U32 numeric values")
def nested_tuple1(ctx, value):
    print(f'that a nested Tuple1 is defined as \(\({value}\) using U32 numeric values')

    ctx.tuple_root_1 = types.CL_Tuple1(types.CL_Tuple1(types.CL_U32(int(value.replace("(", "").replace(")", "")))))


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

    ctx.tuple = get_tuple(int(_tuple), ctx)

    _expected_list = expected.replace('"', '').replace("(", "").replace(")", "").split(",")
    _expected = [int(i.strip()) for i in _expected_list]

    # Pre deploy
    if not hasattr(ctx.tuple, '__iter__'):

        _values = pre_deploy_tuple_values(ctx.tuple, index)

        assert _values == _expected

    # Post deploy
    else:

        _values = post_deploy_get_tuple_values(ctx.tuple, index)

        assert _expected == _values


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

    if hasattr(_bytes_tuple, 'v0'):
        # pre deploy
        assert serialisation.to_bytes(_bytes_tuple).hex() == _bytes
    else:
        # post deploy
        assert _bytes_tuple['bytes'] == _bytes


@given(
    "that a nested Tuple3 is defined as \((.*), (.*), \((.*), (.*), \((.*), (.*), (.*)\)\)\) using U32 numeric values")
def nested_tuple3(ctx, arg0, arg1, arg2, arg3, arg4, arg5, arg6):
    print(
        f'that a nested Tuple3 is defined as \({arg0}, {arg1}, \({arg2}, {arg3}, \({arg4}, {arg5}, {arg6}\)\)\) using U32 numeric values')

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

    ctx.user_1 = '1'
    ctx.user_2 = '2'
    ctx.transfer_amount = 2500000000
    ctx.gas_price = 1
    ctx.ttl = '30m'
    ctx.chain = 'casper-net-1'
    ctx.payment_amount = 100000000

    ctx.cl_values = []
    ctx.cl_values.append({'TUPLE_1': ctx.tuple_root_1})
    ctx.cl_values.append({'TUPLE_2': ctx.tuple_root_2})
    ctx.cl_values.append({'TUPLE_3': ctx.tuple_root_3})

    ctx.tuple_root_1 = ""
    ctx.tuple_root_2 = ""
    ctx.tuple_root_3 = ""

    deploy_set_signatures(ctx)

    ctx.deploy = create_deploy(ctx)

    ctx.sdk_client.send_deploy(ctx.deploy)
    ctx.deploy_result = ctx.deploy

    assert ctx.deploy_result.hash.hex()


@step("the transfer is successful")
def deploy_successful(ctx):
    print(f'the transfer is successful')
    ctx.timeout = 300
    ctx.execution_result = call_async_function(ctx, deploy_event)
    assert ctx.execution_result[0]['result']['Success']

    ctx.deploy = ctx.sdk_client.get_deploy(ctx.deploy_result.hash)
    assert ctx.deploy

    args = ctx.deploy['deploy']['session']['Transfer']['args']
    assert args

    for arg in range(len(args)):
        if args[arg][0] == 'TUPLE_1':
            ctx.tuple_root_1 = args[arg][1]
        if args[arg][0] == 'TUPLE_2':
            ctx.tuple_root_2 = args[arg][1]
        if args[arg][0] == 'TUPLE_3':
            ctx.tuple_root_3 = args[arg][1]

    assert ctx.tuple_root_1
    assert ctx.tuple_root_2
    assert ctx.tuple_root_3


@when("the tuples deploy is obtained from the node")
def tuples_obtained(ctx):
    print(f'the tuples deploy is obtained from the node')
    assert ctx.deploy


def get_tuple(_tuple, ctx):
    if _tuple == 1:
        return ctx.tuple_root_1
    if _tuple == 2:
        return ctx.tuple_root_2
    if _tuple == 3:
        return ctx.tuple_root_3


def pre_deploy_tuple_values(cltype, index) -> list:
    _values: list = []

    func = get_tuple_start_element(cltype, index)
    _methods = ['func.' + attr for attr in dir(func) if attr.startswith('v')]

    for _method in _methods:
        if 'value' in _method:
            _values.append(eval(_method))
        else:
            _values = pre_deploy_iterate_tuple(eval(_method), _values)

    return _values


def post_deploy_get_tuple_values(cltype, index) -> list:
    indx = get_numeric(index)
    _values = []

    if isinstance(cltype['parsed'][indx], list):
        for item in range(len(cltype['parsed'][indx])):
            _values.append(post_deploy_iterate_tuple(cltype['parsed'][indx][item], 0, []))
    else:
        _values.append(post_deploy_iterate_tuple(cltype['parsed'][indx], 0, []))

    return flatten_list(_values)


def post_deploy_iterate_tuple(cltype, start, _values):
    if hasattr(cltype, '__iter__'):
        for item in range(len(cltype)):
            start += 1
            _values.append(post_deploy_iterate_tuple(cltype[item], start, []))
    else:
        return cltype

    return _values


def pre_deploy_iterate_tuple(func, _values) -> list:
    if hasattr(func, 'value'):
        _values.append(func.value)
    else:
        _methods = ['func.' + attr for attr in dir(func) if attr.startswith('v')]
        for _method in _methods:
            pre_deploy_iterate_tuple(eval(_method), _values)

    return _values


def get_tuple_start_element(cltype, index):
    if index == 'first':
        func = cltype.v0
    elif index == 'second':
        func = cltype.v1
    elif index == 'third':
        func = cltype.v2
    else:
        raise ValueError(f'Unknown tuple element: {index}')

    return func


def get_numeric(index):
    if index == 'first':
        return 0
    elif index == 'second':
        return 1
    elif index == 'third':
        return 2
    else:
        raise ValueError(f'Unknown tuple element: {index}')


def flatten_list(_list):
    flat_list = []
    for sublist in _list:
        if isinstance(sublist, list):
            for item in sublist:
                flat_list.append(item)
        else:
            flat_list.append(sublist)

    return flat_list
