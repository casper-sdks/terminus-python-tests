from behave import *

use_step_matcher("re")


@given("that the era summary is requested via the sdk")
def that_era_summary_requested(ctx):
    print('that the era summary is requested via the sdk')

    raise NotImplementedError(u'get_era_summary not implemented')

@then("request the era summary via the node")
def era_summary_requested_via_node(ctx):
    print('that the era summary is requested via the sdk')


@step("the block hash of the returned era summary is equal to the block hash of the test node era summary")
def block_hash_returned_equal(ctx):
    print('the block hash of the returned era summary is equal to the block hash of the test node era summary')


@step("the era of the returned era summary is equal to the era of the returned test node era summary")
def era_returned_equal(ctx):
    print('the era of the returned era summary is equal to the era of the returned test node era summary')


@step("the merkle proof of the returned era summary is equal to the merkle proof of the returned test node era summary")
def merkle_returned_equal(ctx):
    print('the merkle proof of the returned era summary is equal to the merkle proof of the returned test node era '
          'summary')


@step("the state root hash of the returned era summary is equal to the state root hash of the returned test node era "
      "summary")
def state_root_returned_equal(ctx):
    print('the state root hash of the returned era summary is equal to the state root hash of the returned test node '
          'era summary')


@step("the delegators data of the returned era summary is equal to the delegators data of the returned test"
      " node era summary")
def delegators_equal(ctx):
    print('the delegators data of the returned era summary is equal to the delegators data of the returned test node '
          'era summary')

@step("the validators data of the returned era summary is equal to the validators data of the returned test node era"
      " summary")
def validators_equal(ctx):
    print('the validators data of the returned era summary is equal to the validators data of the returned test node '
          'era summary')
