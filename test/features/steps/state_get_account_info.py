from behave import *

from test.features.steps.utils.asyncs import async_rpc_call
from utils.assets import *

use_step_matcher("re")

# Step definitions for state_get_account_info cucumber tests


@given("that the state_get_account_info RCP method is invoked against nctl")
def state_get_account_invoked(ctx):
    print('that the state_get_account_info RCP method is invoked against nctl')

    get_user_hex_public_key(ctx, '1', 'user-1')
    block = async_rpc_call(ctx.sdk_client_rpc.get_block())
    ctx.state_account_info = async_rpc_call(ctx.sdk_client_rpc.get_account_info(ctx.sender_key.account_key.hex(), block))


@then("a valid state_get_account_info_result is returned")
def a_valid_result(ctx):
    print('a valid state_get_account_info_result is returned')

    assert ctx.state_account_info


@step("the state_get_account_info_result contain a valid account hash")
def a_valid_account(ctx):
    print('the state_get_account_info_result contain a valid account hash')

    ctx.user_account = ctx.node_client.get_user_account('user=1')

    # assert ctx.user_account['stored_value']['Account']['account_hash'] == ctx.state_account_info['account_hash']
    assert ctx.user_account['account_hash'] == "account-hash-" + ctx.state_account_info.associated_keys[0].address.hex()


@step("the state_get_account_info_result contain a valid main purse uref")
def a_valid_purse_uref(ctx):
    print('the state_get_account_info_result contain a valid main purse uref')

    assert (ctx.user_account['main_purse'] == "uref-" + ctx.state_account_info.main_purse.address.hex() + "-00" +
            str(ctx.state_account_info.main_purse.access_rights.value))


@step("the state_get_account_info_result contain a valid merkle proof")
def a_valid_merkle_proof(ctx):
    print('the state_get_account_info_result contain a valid merkle proof')
    # TODO SDK to return merkle proof (SDK needs to return higher level json)
    print('TODO SDK to return merkle proof (SDK needs to return higher level json)')


@step("the state_get_account_info_result contain a valid associated keys")
def valid_associated_keys(ctx):
    print('the state_get_account_info_result contain a valid associated keys')

    assert ctx.user_account['associated_keys'][0]['account_hash'] == \
           "account-hash-" + ctx.state_account_info.associated_keys[0].address.hex()


@step("the state_get_account_info_result contain a valid named keys")
def valid_named_keys(ctx):
    print('the state_get_account_info_result contain a valid named keys')

    assert ctx.user_account['named_keys'] == ctx.state_account_info.named_keys


@step("the state_get_account_info_result contain a valid action thresholds")
def valid_action_thresholds(ctx):
    print('the state_get_account_info_result contain a valid action thresholds')

    assert ctx.user_account['action_thresholds']['deployment'] == ctx.state_account_info.action_thresholds.deployment
    assert ctx.user_account['action_thresholds']['key_management'] == ctx.state_account_info.action_thresholds.key_management

