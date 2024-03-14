from behave import *

use_step_matcher("re")

# Step definitions for state_get_auction_info cucumber tests


@given("that the state_get_auction_info RPC method is invoked by hash block identifier")
def state_get_auction_info_invoked(ctx):
    print('that the state_get_auction_info RPC method is invoked by hash block identifier')

    ctx.parent_hash = ctx.sdk_client_rpc.get_block()['header']['parent_hash']

    ctx.state_auction_info_json = ctx.node_requests.get_state_get_auction_info(ctx.parent_hash)['result']
    assert ctx.state_auction_info_json

    ctx.state_get_auction_info_result = ctx.sdk_client_rpc.get_auction_info(ctx.parent_hash)


@then("a valid state_get_auction_info_result is returned")
def a_valid_state_returned(ctx):
    print('a valid state_get_auction_info_result is returned')

    assert ctx.state_get_auction_info_result


@step('the state_get_auction_info_result has and api version of "(.*)"')
def has_valid_api_version(ctx, api_version):
    print('the state_get_auction_info_result has and api version of '.format(api_version))

    assert ctx.state_get_auction_info_result['api_version'] == api_version


@step("the state_get_auction_info_result action_state has a valid state root hash")
def has_valid_state_root_hash(ctx):
    print('the state_get_auction_info_result action_state has a valid state root hash')

    assert ctx.state_get_auction_info_result['auction_state']['state_root_hash'] == \
           ctx.state_auction_info_json['auction_state']['state_root_hash']


@step("the state_get_auction_info_result action_state has a valid height")
def has_valid_height(ctx):
    print('the state_get_auction_info_result action_state has a valid height')

    assert ctx.state_get_auction_info_result['auction_state']['block_height'] == \
           ctx.state_auction_info_json['auction_state']['block_height']


@step("the state_get_auction_info_result action_state has valid bids")
def has_valid_bids(ctx):
    print('the state_get_auction_info_result action_state has valid bids')

    assert ctx.state_get_auction_info_result['auction_state']['bids'] == \
           ctx.state_auction_info_json['auction_state']['bids']


@step("the state_get_auction_info_result action_state has valid era validators")
def has_valid_validators(ctx):
    print('the state_get_auction_info_result action_state has valid era validators')

    assert ctx.state_get_auction_info_result['auction_state']['era_validators'] == \
           ctx.state_auction_info_json['auction_state']['era_validators']


@given("that the state_get_auction_info RPC method is invoked by height block identifier")
def invoked_by_height(ctx):
    print('that the state_get_auction_info RPC method is invoked by height block identifier')

    ctx.parent_hash = ctx.sdk_client_rpc.get_block()['header']['parent_hash']
    ctx.block = ctx.sdk_client_rpc.get_block(ctx.parent_hash)

    ctx.state_auction_info_json = ctx.node_requests.get_state_get_auction_info(ctx.parent_hash)['result']
    assert ctx.state_auction_info_json

    ctx.state_get_auction_info_result = ctx.sdk_client_rpc.get_auction_info(ctx.block['header']['height'])


@given("that the state_get_auction_info RPC method is invoked by an invalid block hash identifier")
def invoked_by_invalid_hash(ctx):
    print('that the state_get_auction_info RPC method is invoked by an invalid block hash identifier')

    try:
        ctx.sdk_client_rpc.get_auction_info('9608b4b7029a18ae35373eab879f523850a1b1fd43a3e6da774826a343af4ad2')
    except Exception as ex:
        ctx.exception = ex


@then("an error code of (.*) is returned")
def error_code_is_returned(ctx, error_code):
    print('an error code of {} is returned'.format(error_code))

    assert ctx.exception.args[0].code == int(error_code)


@step('an error message of "(.*)" is returned')
def error_message_is_returned(ctx, error_msg):
    print('an error message of "{}" is returned'.format(error_msg))

    assert ctx.exception.args[0].message == error_msg
