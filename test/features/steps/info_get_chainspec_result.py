from behave import *

from test.features.steps.utils.asyncs import async_rpc_call

use_step_matcher("re")

# Step definitions for info_get_chainspec cucumber tests


@given("that the info_get_chainspec is invoked using a simple RPC json request")
def the_info_get_chainspec_is_invoked_rpc(ctx):
    print('that the info_get_chainspec is invoked using a simple RPC json request')

    ctx.chain_spec_rpc = ctx.node_requests.get_chain_spec()
    assert ctx.chain_spec_rpc


@step("that info_get_chainspec is invoked against the SDK")
def the_info_get_chainspec_is_invoked_sdk(ctx):
    print('that info_get_chainspec is invoked against the SDK')

    ctx.chain_spec_sdk = async_rpc_call(ctx.sdk_client_rpc.get_chainspec())
    assert ctx.chain_spec_sdk


@then("the SDK chain bytes equals the RPC json request chain bytes")
def chain_bytes_equal(ctx):
    print('the SDK chain bytes equals the RPC json request chain bytes')

    assert ctx.chain_spec_sdk['chainspec_bytes'] == ctx.chain_spec_rpc['result']['chainspec_bytes']['chainspec_bytes']


@step("the SDK genesis bytes equals the RPC json request genesis bytes")
def genesis_bytes_equal(ctx):
    print('the SDK genesis bytes equals the RPC json request genesis bytes')

    if ctx.chain_spec_sdk['maybe_genesis_accounts_bytes'] is not None:
        assert ctx.chain_spec_sdk['maybe_genesis_accounts_bytes'] == ctx.chain_spec_rpc['result']['chainspec_bytes']['maybe_genesis_accounts_bytes']
    else:
        assert ctx.chain_spec_rpc['result']['chainspec_bytes']['maybe_genesis_accounts_bytes'] is None


@step("the SDK global state bytes equals the RPC json request global state bytes")
def global_state_equals(ctx):
    print('the SDK global state bytes equals the RPC json request global state bytes')

    if ctx.chain_spec_sdk['maybe_global_state_bytes'] is not None:
        assert ctx.chain_spec_sdk['maybe_global_state_bytes'] == ctx.chain_spec_rpc['result']['chainspec_bytes']['maybe_global_state_bytes']
    else:
        assert ctx.chain_spec_rpc['result']['chainspec_bytes']['maybe_global_state_bytes'] is None

