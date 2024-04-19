from behave import *

from pycspr import parse_public_key
from pycspr.types.node.rpc import GlobalStateID, GlobalStateIDType, PurseIDType, PurseID

from test.features.steps.utils.assets import get_user_asset_path

use_step_matcher("re")


# Step definitions for state_get_balance cucumber tests


@given("that the state_get_balance RPC method is invoked against nclt user-1 purse")
def state_get_balance_invoked(ctx):
    print('that the state_get_balance RPC method is invoked against nclt user-1 purse')

    ctx.state_root_hash = ctx.node_client.get_state_root_hash(1)
    account_key = parse_public_key(get_user_asset_path(ctx.ASSETS_ROOT, "1", "user-1", "public_key_hex")).account_key

    ctx.account_main_purse = \
        ctx.sdk_client_rpc.get_account_main_purse_uref(account_key)

    global_state_id = GlobalStateID(ctx.state_root_hash, GlobalStateIDType.STATE_ROOT_HASH)
    purse_id = PurseID(ctx.account_main_purse, PurseIDType.UREF)

    ctx.state_get_balance_result = ctx.sdk_client_rpc.get_account_balance(purse_id, global_state_id)

    assert ctx.state_get_balance_result


@then("a valid state_get_balance_result is returned")
def valid_result_returned(ctx):
    print('a valid state_get_balance_result is returned')

    assert ctx.state_get_balance_result


@step("the state_get_balance_result contains the purse amount")
def contains_purse_amount(ctx):
    print('the state_get_balance_result contains the purse amount')

    json = ctx.node_requests.get_state_get_balance(ctx.state_root_hash, ctx.node_client.get_account_main_purse('user=1'))
    assert json

    balance = json["result"]["balance_value"]
    assert balance

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
