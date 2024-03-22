from behave import *

from test.features.steps.utils.validate import validate_merkle_proofs

use_step_matcher("re")


@given("that the era summary is requested via the sdk")
def that_era_summary_requested(ctx):
    print('that the era summary is requested via the sdk')

    block = ctx.sdk_client_rpc.get_block()
    assert block
    ctx.block_hash = block['hash']

    ctx.sdk_err_summary = ctx.sdk_client_rpc.get_era_summary(ctx.block_hash)
    assert ctx.sdk_err_summary

@then("request the era summary via the node")
def era_summary_requested_via_node(ctx):
    print('that the era summary is requested via the sdk')

    ctx.node_err_summary = ctx.node_client.get_era_summary()
    assert ctx.node_err_summary


@step("the block hash of the returned era summary is equal to the block hash of the test node era summary")
def block_hash_returned_equal(ctx):
    print('the block hash of the returned era summary is equal to the block hash of the test node era summary')

    assert ctx.node_err_summary['era_summary']['block_hash'] == ctx.sdk_err_summary.block_hash.hex()


@step("the era of the returned era summary is equal to the era of the returned test node era summary")
def era_returned_equal(ctx):
    print('the era of the returned era summary is equal to the era of the returned test node era summary')

    assert ctx.node_err_summary['era_summary']['era_id'] == ctx.sdk_err_summary.era_id


@step("the merkle proof of the returned era summary is equal to the merkle proof of the returned test node era summary")
def merkle_returned_equal(ctx):
    print('the merkle proof of the returned era summary is equal to the merkle proof of the returned test node era '
          'summary')

    validate_merkle_proofs(ctx.node_err_summary['era_summary']['merkle_proof'],
                           ctx.sdk_err_summary.merkle_proof.hex())


@step("the state root hash of the returned era summary is equal to the state root hash of the returned test node era "
      "summary")
def state_root_returned_equal(ctx):
    print('the state root hash of the returned era summary is equal to the state root hash of the returned test node '
          'era summary')

    assert ctx.node_err_summary['era_summary']['state_root_hash'] == ctx.sdk_err_summary.state_root.hex()


@step("the delegators data of the returned era summary is equal to the delegators data of the returned test"
      " node era summary")
def delegators_equal(ctx):
    print('the delegators data of the returned era summary is equal to the delegators data of the returned test node '
          'era summary')
    # TODO Iterate results and compare delegators

    assert len(ctx.node_err_summary['era_summary']['stored_value']['EraInfo']['seigniorage_allocations']) \
        == len(ctx.sdk_err_summary.era_info.seigniorage_allocations)


@step("the validators data of the returned era summary is equal to the validators data of the returned test node era"
      " summary")
def validators_equal(ctx):
    print('the validators data of the returned era summary is equal to the validators data of the returned test node '
          'era summary')
    # TODO Iterate results and compare validators

    assert len(ctx.node_err_summary['era_summary']['stored_value']['EraInfo']['seigniorage_allocations']) \
        == len(ctx.sdk_err_summary.era_info.seigniorage_allocations)
