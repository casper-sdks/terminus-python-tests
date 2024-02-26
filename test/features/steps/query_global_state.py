from behave import *
from pycspr import types

from test.features.steps.utils.asyncs import call_async_function, block_event
from test.features.steps.utils.deploy import deploy_to_chain, deploy_set_signatures

use_step_matcher("re")

# Step definitions for query_global_state cucumber tests


@given("that a valid block hash is known")
def a_valid_block_hash_is_known(ctx):
    print('that a valid block hash is known')

    deploy_set_signatures(ctx)

    ctx.transfer_amount = 2500000000
    ctx.payment_amount = 10000000
    ctx.chain = 'cspr-dev-cctl'
    ctx.ttl = '30m'
    ctx.gas_price = 1

    ctx.deploy_result = deploy_to_chain(ctx)
    ctx.timeout = float(300)
    ctx.last_block_added = call_async_function(ctx, block_event)

    assert ctx.last_block_added


@when("the query_global_state RCP method is invoked with the block hash as the query identifier")
def query_global_state_rcp_invoked(ctx):
    print('the query_global_state RCP method is invoked with the block hash as the query identifier')

    # key = f'deploy-{ctx.deploy_result.hash.hex()}'
    key = ctx.deploy_result.hash.hex()
    # key = ctx.deploy_result.hash
    block_hash = ctx.last_block_added['BlockAdded']['block_hash']

    # types.GlobalStateIDType

    state_id = types.GlobalStateID(
        block_hash,
        types.GlobalStateIDType.BLOCK
    )

    cl_key = types.CL_Key.from_string('account-hash-' + ctx.deploy_result.header.account_public_key.account_hash.hex())

    # Fails because the query_global_state SDK method is passing a dict instead of a string value as part of the params
    # {
    #     "id": "383766003",
    #     "jsonrpc": "2.0",
    #     "method": "query_global_state",
    #     "params": {
    #         "state_identifier": {
    #             "BlockHash": "042074ad78585bd077a0a669bb64f647bbd221f8e81997cadab59a54058e0ad6"
    #         },
    #         "key": "account-hash-98f380B97c33C4ea4a70B9Be7830fA59834E68Da8F2BBf17d2652fb22180aE19",
    #         "path": []
    #     }
    # }
    # state_identifier and key are returned as dicts in get_query_global_state_params

    ctx.global_state_data = ctx.sdk_client.query_global_state(cl_key, '[]', state_id)

    assert ctx.global_state_data

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
    raise NotImplementedError('query_global_state not implemented')


@when(
    "the query_global_state RCP method is invoked with the state root hash as the query identifier and an invalid key")
def the_rcp_method_invoked_with_invalid_key(ctx):
    print('the query_global_state RCP method is invoked with the state root hash as the query identifier and an '
          'invalid key')


@given("the query_global_state RCP method is invoked with an invalid block hash as the query identifier")
def rcp_invoked_with_invalid_block_hash(ctx):
    print('the query_global_state RCP method is invoked with an invalid block hash as the query identifier')

    raise NotImplementedError('query_global_state not implemented')
