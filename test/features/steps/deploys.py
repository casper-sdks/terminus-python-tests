from behave import *

from utils.assets import *
from utils.asyncs import *
from utils.deploy import *
from utils.validate import *

use_step_matcher("re")

# Step Definitions for Deploys Cucumber Tests

@given('that user-"(.*)" initiates a transfer to user-"(.*)"')
def step_impl(ctx, user_1, user_2):
    print("that user-{} initiates a transfer to user- {}".format(user_1, user_2))

    ctx.user_1 = user_1
    ctx.user_2 = user_2



@step('the transfer amount is "(.*)"')
def step_impl(ctx, amount):
    print("the transfer amount is {}".format(amount))

    ctx.transfer_amount = int(amount)


@step('the transfer gas price is "(.*)"')
def step_impl(ctx, gas):
    print("the transfer gas price is {}".format(gas))

    ctx.gas_price = int(gas)


@step('the deploy is given a ttl of "(.*)"')
def step_impl(ctx, ttl):
    print("the deploy is given a ttl of {}".format(ttl))

    ctx.ttl = ttl


@when('the deploy is put on chain "(.*)"')
def step_impl(ctx, chain):
    print("the deploy is put on chain {}".format(chain))

    ctx.chain = chain

    ctx.deploy_result = deploy_to_chain(ctx)


@then('the deploy response contains a valid deploy hash of length "(.*)" and an API version "(.*)"')
def step_impl(ctx, hash_length, api):
    print(
        "the deploy response contains a valid deploy hash of length {} and an API version {}".format(hash_length, api))

    assert ctx.deploy_result
    assert ctx.deploy_result.hash.hex()
    assert len(ctx.deploy_result.hash.hex()) is int(hash_length)
    # TODO api version not returned in deploy response


@then('wait for a block added event with a timeout of "(.*)" seconds')
def step_impl(ctx, timeout):
    print("wait for a block added event with a timeout of {} seconds".format(timeout))

    ctx.timeout = float(timeout)
    ctx.transfer_block_sdk = call_async_function(ctx, block_event)

    assert ctx.deploy_result.hash.hex() in ctx.transfer_block_sdk['BlockAdded']['block']['body']['transfer_hashes']


@given("that a Transfer has been successfully deployed")
def step_impl(ctx):
    print('that a Transfer has been successfully deployed')

    ctx.user_1 = '1'
    ctx.user_2 = '2'
    ctx.transfer_amount = 2500000000
    ctx.gas_price = 1
    ctx.ttl = '30m'
    ctx.chain = 'casper-net-1'

    ctx.deploy_result = deploy_to_chain(ctx)

    assert ctx.deploy_result

@when("a deploy is requested via the info_get_deploy RCP method")
def step_impl(ctx):
    print('a deploy is requested via the info_get_deploy RCP method')

    ctx.timeout = 300
    ctx.transfer_block_sdk = call_async_function(ctx, block_event)

    ctx.deploy = ctx.sdk_client.get_deploy(ctx.deploy_result.hash.hex())
    assert ctx.deploy


@then('the deploy data has an API version of "(.*)"')
def step_impl(ctx, api):
    print('the deploy data has an API version of '.format(api))
    assert ctx.deploy['api_version'] == api

@step('the deploy execution result has "lastBlockAdded" block hash')
def step_impl(ctx):
    print('the deploy execution result has "lastBlockAdded" block hash')

    assert ctx.transfer_block_sdk['BlockAdded']['block_hash'] == ctx.deploy['execution_results'][0]['block_hash']

@step('the deploy execution has a cost of "(.*)" motes')
def step_impl(ctx, motes):
    print('the deploy execution has a cost of {} motes'.format(motes))

    assert ctx.deploy['execution_results'][0]['result']['Success']['cost'] == motes

@step('the deploy has a payment amount of "(.*)"')
def step_impl(ctx, amount):
    print('the deploy has a payment amount of {}'.format(amount))

    assert ctx.deploy['deploy']['payment']['ModuleBytes']['args'][0][1]['cl_type'] == 'U512'
    assert ctx.deploy['deploy']['payment']['ModuleBytes']['args'][0][1]['parsed'] == amount


@step("the deploy has a valid hash")
def step_impl(ctx):
    print('the deploy has a valid hash')

    assert len(ctx.deploy_result.hash.hex()) == 64
    assert ctx.deploy_result.hash.hex() == ctx.deploy['deploy']['hash']

@step("the deploy has a valid timestamp")
def step_impl(ctx):
    print('the deploy has a valid timestamp')
    print(ctx.deploy)
    print(ctx.deploy_result)

    assert compare_timestamps(ctx.deploy_result.header.timestamp.value, ctx.deploy['deploy']['header']['timestamp'])


@step("the deploy has a valid body hash")
def step_impl(ctx):
    print('the deploy has a valid body hash')

    assert ctx.deploy_result.header.body_hash.hex() == ctx.deploy['deploy']['header']['body_hash']


@step('the deploy has a session type of "Transfer"')
def step_impl(ctx):
    print('the deploy has a session type of Transfer')

    assert type(ctx.deploy_result.session) == pycspr.types.deploys.Transfer



@step("the deploy is approved by user-1")
def step_impl(ctx):
    print('the deploy is approved by user-1')

    assert len(ctx.deploy_result.approvals) == 1
    key = get_user_asset(ctx.ASSETS_ROOT, "1", "1", "public_key.pem")

    ctx.deploy_result.approvals[0].signer.account_key.hex()

    print(key)




@step("the deploy has a gas price of 1")
def step_impl(ctx):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And the deploy has a gas price of 1')


@step("the deploy has a ttl of 30m")
def step_impl(ctx):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And the deploy has a ttl of 30m')


@step('the deploy session has a "amount" argument value of type "U512"')
def step_impl(ctx):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And the deploy session has a "amount" argument value of type "U512"')


@step('the deploy session has a "amount" argument with a numeric value of 2500000000')
def step_impl(ctx):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(
        u'STEP: And the deploy session has a "amount" argument with a numeric value of 2500000000')


@step('the deploy session has a "target" argument with the public key of user-2')
def step_impl(ctx):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And the deploy session has a "target" argument with the public key of user-2')


@step('the deploy session has a "target" argument value of type "PublicKey"')
def step_impl(ctx):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And the deploy session has a "target" argument value of type "PublicKey"')


@step('the deploy session has a "id" argument value of type "Option"')
def step_impl(ctx):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: And the deploy session has a "id" argument value of type "Option"')