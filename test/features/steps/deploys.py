import random

import pycspr
from behave import *
from pycspr import *
from pycspr.types import Deploy

from utils.assets import *
from utils.asyncs import *

use_step_matcher("re")

# Step Definitions for Deploys Cucumber Tests

@given('that user-"(.*)" initiates a transfer to user-"(.*)"')
def step_impl(ctx, user_1, user_2):
    print("that user-{} initiates a transfer to user- {}".format(user_1, user_2))

    ctx.sender_key = pycspr.parse_private_key(
        get_user_asset_path(ctx.ASSETS_ROOT, "1", user_1, "secret_key.pem"),
        KeyAlgorithm.ED25519.name,
    )
    ctx.receiver_key = pycspr.parse_public_key(
        get_user_asset_path(ctx.ASSETS_ROOT, "1", user_2, "public_key_hex")
    )


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

    deploy: Deploy

    deploy_params = pycspr.create_deploy_parameters(
        account=ctx.sender_key,
        chain_name=chain,
        ttl=ctx.ttl,
        gas_price=ctx.gas_price
    )

    # Set deploy.
    deploy = pycspr.create_transfer(
        params=deploy_params,
        amount=ctx.transfer_amount,
        target=ctx.receiver_key.account_key,
        correlation_id=random.randint(1, 1e6)
    )

    deploy.approve(ctx.sender_key)

    ctx.sdk_client.send_deploy(deploy)

    ctx.deploy_result = deploy


@then('the deploy response contains a valid deploy hash of length "(.*)" and an API version "(.*)"')
def step_impl(ctx, hash_length, api):
    print(
        "the deploy response contains a valid deploy hash of length {} and an API version {}".format(hash_length, api))

    assert ctx.deploy_result
    assert ctx.deploy_result.hash.hex()
    assert len(ctx.deploy_result.hash.hex()) is int(hash_length)
    # TODO api version not returned in deploy response


@then('wait for a block added event with a timout of "(.*)" seconds')
def step_impl(ctx, timeout):
    print("wait for a block added event with a timout of {}".format(timeout))

    ctx.timeout = float(timeout)
    ctx.transfer_block_sdk = call_async_function(ctx, block_event)

    assert ctx.deploy_result.hash.hex() in ctx.transfer_block_sdk['BlockAdded']['block']['body']['transfer_hashes']
