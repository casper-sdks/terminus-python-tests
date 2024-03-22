from behave import *

use_step_matcher("re")

# Step definitions for info_get_status cucumber tests

@given("that the info_get_status is invoked against nctl")
def info_get_status_invoked(ctx):
    print('that the info_get_status is invoked against nctl')

    ctx.expected_status_data = ctx.node_client.get_node_status(1)
    assert ctx.expected_status_data

    ctx.status_data = ctx.sdk_client_rpc.get_node_status()


@then("an info_get_status_result is returned")
def info_get_status_is_returned(ctx):
    print('an info_get_status_result is returned')
    assert ctx.status_data


@step('the info_get_status_result api_version is "(.*)"')
def api_version_is(ctx, api):
    print('the info_get_status_result api_version is {}'.format(api))
    assert ctx.status_data['api_version'] == api


@step('the info_get_status_result chainspec_name is "(.*)"')
def chaninspec_name_is(ctx, chain):
    print('the info_get_status_result chainspec_name is {}'.format(chain))
    assert ctx.status_data['chainspec_name'] == ctx.chain_name


@step("the info_get_status_result has a valid last_added_block_info")
def has_a_valid_last_block(ctx):
    print('the info_get_status_result has a valid last_added_block_info')

    assert ctx.expected_status_data['last_added_block_info'] == ctx.status_data['last_added_block_info']


@step("the info_get_status_result has a valid our_public_signing_key")
def has_a_valid_public_signing_key(ctx):
    print('the info_get_status_result has a valid our_public_signing_key')

    assert ctx.expected_status_data['our_public_signing_key'] == ctx.status_data['our_public_signing_key']


@step("the info_get_status_result has a valid starting_state_root_hash")
def valid_starting_state_root_hash(ctx):
    print('the info_get_status_result has a valid starting_state_root_hash')

    assert ctx.expected_status_data['starting_state_root_hash'] == ctx.status_data['starting_state_root_hash']


@step("the info_get_status_result has a valid build_version")
def has_a_valid_build_version(ctx):
    print('the info_get_status_result has a valid build_version')

    assert ctx.expected_status_data['build_version'] == ctx.status_data['build_version']


@step("the info_get_status_result has a valid round_length")
def has_a_valid_round_length(ctx):
    print('the info_get_status_result has a valid round_length')

    assert ctx.expected_status_data['round_length'] == ctx.status_data['round_length']


@step("the info_get_status_result has a valid uptime")
def has_a_valid_uptime(ctx):
    print('the info_get_status_result has a valid uptime')

    assert ctx.status_data['uptime']
    assert 's' in ctx.status_data['uptime']
    assert 'ms' in ctx.status_data['uptime']


@step("the info_get_status_result has a valid peers")
def has_valid_peers(ctx):
    print('the info_get_status_result has a valid peers')

    assert ctx.expected_status_data['peers'] == ctx.status_data['peers']
