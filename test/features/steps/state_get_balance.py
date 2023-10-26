from behave import *

from pycspr import types

use_step_matcher("re")


# Step definitions for state_get_balance cucumber tests


@given("that the state_get_balance RPC method is invoked against nclt user-1 purse")
def state_get_balance_invoked(ctx):
    print('that the state_get_balance RPC method is invoked against nclt user-1 purse')

    ctx.state_root_hash = ctx.nctl_client.get_state_root_hash(1)
    ctx.account_main_purse = ctx.nctl_client.get_account_main_purse('user=1')

    ctx.state_get_balance_result = ctx.sdk_client.get_account_balance(
        types.CL_URef(types.CL_URefAccessRights.READ_ADD_WRITE,
                      bytes.fromhex(ctx.account_main_purse[5:-4])),
        ctx.state_root_hash)


@then("a valid state_get_balance_result is returned")
def valid_result_returned(ctx):
    print('a valid state_get_balance_result is returned')

    assert ctx.state_get_balance_result


@step("the state_get_balance_result contains the purse amount")
def contains_purse_amount(ctx):
    print('the state_get_balance_result contains the purse amount')

    json = ctx.nctl_requests.get_state_get_balance(ctx.state_root_hash, ctx.account_main_purse)
    balance = json["result"]["balance_value"]

    assert ctx.state_get_balance_result == int(balance)


@step('the state_get_balance_result contains api version "(.*)"')
def contains_api_version(ctx, api_version):
    print('the state_get_balance_result contains api version "{}"'.format(api_version))

    # TODO SDK to return api version (SDK needs to return higher level json)
    print('TODO SDK to return api version (SDK needs to return higher level json)')


@step("the state_get_balance_result contains a valid merkle proof")
def contains_valid_merkle_proof(ctx):
    print('the state_get_balance_result contains a valid merkle proof')

    # TODO SDK to return merkle proof (SDK needs to return higher level json)
    print('TODO SDK to return merkle proof (SDK needs to return higher level json)')
