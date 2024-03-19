from behave import *

from utils.asyncs import *
from utils.deploy import *
from utils.validate import *

use_step_matcher("re")


# Step Definitions for Deploys Cucumber Tests

@given('that user-(.*) initiates a transfer to user-(.*)')
def that_a_user_initiates_a_transfer_to_another_user(ctx, user_1, user_2):
    print("that user-{} initiates a transfer to user-{}".format(user_1, user_2))

    ctx.user_1 = user_1
    ctx.user_2 = user_2


@step('the transfer amount is (.*)')
def the_transfer_amount_is(ctx, amount):
    print("the transfer amount is {}".format(amount))

    ctx.transfer_amount = int(amount)


@step('the transfer gas price is (.*)')
def the_transfer_gas_price_is(ctx, gas):
    print("the transfer gas price is {}".format(gas))

    ctx.gas_price = int(gas)


@step('the deploy is given a ttl of (.*)m')
def the_deply_is_given_a_ttl_of(ctx, ttl):
    print("the deploy is given a ttl of {}".format(ttl + "m"))

    ctx.ttl = ttl + 'm'


@when('the deploy is put on chain "(.*)"')
def the_deploy_is_put_on_chain(ctx, chain):
    print("the deploy is put on chain {}".format(chain))

    ctx.chain = chain
    ctx.payment_amount = 10000

    deploy_set_signatures(ctx)
    ctx.deploy_result = deploy_to_chain(ctx)

    print(ctx.deploy_result)


@then('the deploy response contains a valid deploy hash of length (.*) and an API version "(.*)"')
def the_deploy_response_contains_a_valid_hash_and_a_valid_api_version(ctx, hash_length, api):
    print(
        "the deploy response contains a valid deploy hash of length {} and an API version {}".format(hash_length, api))

    assert ctx.deploy_result
    assert ctx.deploy_result.hash.hex()
    assert len(ctx.deploy_result.hash.hex()) is int(hash_length)
    # TODO api version not returned in deploy response


@then('wait for a block added event with a timeout of (.*) seconds')
def wait_for_block_added_event(ctx, timeout):
    print("wait for a block added event with a timeout of {} seconds".format(timeout))

    ctx.timeout = float(timeout)
    ctx.last_block_added = call_async_function(ctx, block_event)
    ctx.param_map['last_block_added'] = ctx.last_block_added
    assert ctx.deploy_result.hash.hex() in ctx.last_block_added['BlockAdded']['block']['body']['transfer_hashes']


@given("that a Transfer has been successfully deployed")
def a_transfer_is_successful(ctx):
    print('that a Transfer has been successfully deployed')

    ctx.user_1 = '1'
    ctx.user_2 = '2'
    ctx.transfer_amount = 2500000000
    ctx.gas_price = 1
    ctx.ttl = '30m'
    ctx.payment_amount = 100000000

    deploy_set_signatures(ctx)
    ctx.deploy_result = deploy_to_chain(ctx)

    assert ctx.deploy_result


@when("a deploy is requested via the info_get_deploy RCP method")
def a_deploy_is_requested(ctx):
    print('a deploy is requested via the info_get_deploy RCP method')

    ctx.timeout = 300
    ctx.last_block_added = call_async_function(ctx, block_event)
    ctx.param_map['last_block_added'] = ctx.last_block_added

    ctx.deploy = ctx.sdk_client_rpc.get_deploy(ctx.deploy_result.hash.hex())
    assert ctx.deploy


@then('the deploy data has an API version of "(.*)"')
def the_deploy_has_api_version(ctx, api):
    print('the deploy data has an API version of '.format(api))
    assert ctx.deploy['api_version'] == api


@step('the deploy execution result has "(.*)" block hash')
def the_deploy_has_a_specific_block_hash(ctx, block):
    print('the deploy execution result has {} block hash'.format(block))

    assert ctx.param_map[ctx.param_keys[block]]['BlockAdded']['block_hash'] == ctx.deploy['execution_results'][0]['block_hash']


@step('the deploy execution has a cost of (.*) motes')
def the_deploy_has_execution_cost_of(ctx, motes):
    print('the deploy execution has a cost of {} motes'.format(motes))

    assert ctx.deploy['execution_results'][0]['result']['Success']['cost'] == motes


@step('the deploy has a payment amount of (.*)')
def the_deploy_has_payment_amount_of(ctx, amount):
    print('the deploy has a payment amount of {}'.format(amount))

    assert ctx.deploy['deploy']['payment']['ModuleBytes']['args'][0][1]['cl_type'] == 'U512'
    assert ctx.deploy['deploy']['payment']['ModuleBytes']['args'][0][1]['parsed'] == amount


@step("the deploy has a valid hash")
def the_deploy_has_a_valid_hash(ctx):
    print('the deploy has a valid hash')

    assert len(ctx.deploy_result.hash.hex()) == 64
    assert ctx.deploy_result.hash.hex() == ctx.deploy['deploy']['hash']


@step("the deploy has a valid timestamp")
def the_deploy_has_a_valid_timestamp(ctx):
    print('the deploy has a valid timestamp')

    assert compare_timestamps(ctx.deploy_result.header.timestamp.value, ctx.deploy['deploy']['header']['timestamp'])


@step("the deploy has a valid body hash")
def the_deploy_has_a_valid_body_hash(ctx):
    print('the deploy has a valid body hash')

    assert ctx.deploy_result.header.body_hash.hex() == ctx.deploy['deploy']['header']['body_hash']


@step('the deploy has a session type of "(.*)"')
def the_deploy_(ctx, _type):
    print('the deploy has a session type of {}'.format(_type))

    assert type(ctx.deploy_result.session) == ctx.values_map[_type]


@step('the deploy is approved by user-(.*)')
def the_deploy_is_approved(ctx, user):
    print('the deploy is approved by user-{}'.format(user))

    assert len(ctx.deploy_result.approvals) == 1

    user_1_key = pycspr.parse_public_key(
        ctx.get_user_asset_path(ctx.ASSETS_ROOT, "1", 'user-{}'.format(user), "public_key_hex")
    )

    assert user_1_key == ctx.deploy_result.approvals[0].signer


@step('the deploy has a gas price of (.*)')
def the_deploy_has_a_gas_price_of(ctx, gas_price):
    print("the deploy has a gas price of {}".format(gas_price))

    assert ctx.deploy_result.header.gas_price == int(gas_price)


@step('the deploy has a ttl of (.*)m')
def the_deploy_has_a_ttl_of(ctx, ttl):
    print("the deploy has a ttl of {}".format(ttl + "m"))

    assert ctx.deploy_result.header.ttl.humanized == ttl + 'm'


@step('the deploy session has a "(.*)" argument with a numeric value of "(.*)"')
def the_deploy_session_argument_has_a_numeric_value_of(ctx, arg, value):
    print('the deploy session has a {} argument with a numeric value of {}'.format(arg, value))

    assert ctx.deploy_result.session.args[arg].value == int(value)


@step('the deploy session has a "(.*)" argument with the public key of user-(.*)')
def the_deploy_session_argument_has_public_key_of_a_use(ctx, arg, user):
    print('the deploy session has a {} argument with the public key of user-{}'.format(arg, user))

    user_key = pycspr.parse_public_key(
        ctx.get_user_asset_path(ctx.ASSETS_ROOT, "1", 'user-{}'.format(user), "public_key_hex")
    )

    assert user_key == ctx.deploy_result.session.args[arg]


@step('the deploy session has a "(.*)" argument value of type "(.*)"')
def teh_deploy_session_argument_has_a_type_of(ctx, arg, _type):
    print('the deploy session has a {} argument value of type {}'.format(arg, _type))

    assert type(ctx.deploy_result.session.args[arg]) == ctx.values_map[_type]
