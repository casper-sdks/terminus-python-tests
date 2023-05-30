from behave import *

use_step_matcher("re")


@given("that a valid block hash is known")
def a_valid_block_hash_is_known(ctx):
    raise NotImplementedError('Feature not implemented')


@when("the query_global_state RCP method is invoked with the block hash as the query identifier")
def query_global_state_rcp_invoked(ctx):
    print('the query_global_state RCP method is invoked with the block hash as the query identifier')


@then("a valid query_global_state_result is returned")
def valid_state_result_returned(ctx):
    print('a valid query_global_state_result is returned')


@step("the query_global_state_result contains a valid deploy info stored value")
def state_contains_valid_deploy(ctx):
    print('the query_global_state_result contains a valid deploy info stored value')


@step("the query_global_state_result's stored value from is the user-(.*) account hash")
def the_result_is_the_users_hash(ctx, user):
    print("the query_global_state_result's stored value from is the user-{} account hash".format(user))


@step("the query_global_state_result's stored value contains a gas price of (.*)")
def the_result_contains_gas_price_of(ctx, gas):
    print("the query_global_state_result's stored value contains a gas price of {}".format(gas))


@step("the query_global_state_result stored value contains the transfer hash")
def the_result_contains_the_transfer_hash(ctx):
    print('the query_global_state_result stored value contains the transfer hash')


@step("the query_global_state_result stored value contains the transfer source uref")
def the_result_contains_the_uref(ctx):
    print('the query_global_state_result stored value contains the transfer source uref')


@given("that the state root hash is known")
def the_state_root_hash_is_known(ctx):
    print('that the state root hash is known')


@when(
    "the query_global_state RCP method is invoked with the state root hash as the query identifier and an invalid key")
def the_rcp_method_invoked_with_invalid_key(ctx):
    print('the query_global_state RCP method is invoked with the state root hash as the query identifier and an '
          'invalid key')


@then("an error code of (.*) is returned")
def error_code_is_returned(ctx, error_code):
    print('an error code of {} is returned'.format(error_code))


@step('an error message of "(.*)" is returned')
def error_message_is_returned(ctx, error_msg):
    print('an error message of "{}" is returned'.format(error_msg))


@given("the query_global_state RCP method is invoked with an invalid block hash as the query identifier")
def rcp_invoked_with_invalid_block_hash(ctx):
    print('the query_global_state RCP method is invoked with an invalid block hash as the query identifier')
