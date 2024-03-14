from behave import *

use_step_matcher("re")

# Step definitions for get_chain_state_root_hash cucumber tests


@given("that the chain_get_state_root_hash RCP method is invoked against nctl")
def the_chain_state_root_hash_is_invoked_against_nctl(ctx):
    print('that the chain_get_state_root_hash RCP method is invoked against nctl')

    ctx.state_root_hash = ctx.sdk_client_rpc.get_state_root_hash()
    assert ctx.state_root_hash


@then("a valid chain_get_state_root_hash_result is returned")
def a_valid_state_root_hash_is_returned(ctx):
    print('a valid chain_get_state_root_hash_result is returned')

    expected_state_root_hash = ctx.node_client.get_state_root_hash(1)
    assert expected_state_root_hash
    assert ctx.state_root_hash.hex() in expected_state_root_hash
