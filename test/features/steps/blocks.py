import codecs
import random

import pycspr
from behave import *
from pycspr import *
from pycspr.types import Deploy

from utils.assets import *
from utils.asyncs import *
from utils.validate import *

# Step Definitions for Block Cucumber Tests


INVALID_BLOCK_HASH = "2fe9630b7790852e4409d815b04ca98f37effcdf9097d317b9b9b8ad658f47c8"
INVALID_HEIGHT = 9999999999
BLOCK_ERR_MSG = "block not known"
BLOCK_ERR_CODE = -32001


@given("that the latest block is requested via the sdk")
def step_impl(ctx):
    print("that the latest block is requested via the sdk")
    ctx.blockDataSdk = ctx.sdk_client.get_block()


@then('request the latest block via the test node')
def step_impl(ctx):
    print("request the latest block via the test node")
    ctx.blockDataNode = ctx.nctl_client.get_latest_block()


@then("the body of the returned block is equal to the body of the returned test node block")
def step_impl(ctx):
    print("the body of the returned block is equal to the body of the returned test node block")

    assert len(ctx.blockDataSdk['body']) > 0
    assert ctx.blockDataSdk['body']['proposer'] == ctx.blockDataNode['body']['proposer']
    assert ctx.blockDataSdk['body']['deploy_hashes'] == ctx.blockDataNode['body']['deploy_hashes']
    assert ctx.blockDataSdk['body']['transfer_hashes'] == ctx.blockDataNode['body']['transfer_hashes']


@step("the hash of the returned block is equal to the hash of the returned test node block")
def step_impl(ctx):
    print("the hash of the returned block is equal to the hash of the returned test node block")

    assert ctx.blockDataSdk['hash'] == ctx.blockDataNode['hash']


@step("the header of the returned block is equal to the header of the returned test node block")
def step_impl(ctx):
    print("the header of the returned block is equal to the header of the returned test node block")

    assert ctx.blockDataSdk['header'] == ctx.blockDataNode['header']


@step("the proofs of the returned block are equal to the proofs of the returned test node block")
def step_impl(ctx):
    print("the proofs of the returned block are equal to the proofs of the returned test node block")

    assert ctx.blockDataSdk['proofs'] == ctx.blockDataNode['proofs']


@given("that a block is returned by hash via the sdk")
def step_impl(ctx):
    ctx.blockDataSdk = ctx.sdk_client.get_block()
    ctx.blockDataSdk = ctx.sdk_client.get_block(ctx.blockDataSdk['hash'])


@then("request a block by hash via the test node")
def step_impl(ctx):
    print("request a block by hash via the test node")

    ctx.blockDataNode = ctx.nctl_client.get_latest_block_by_param("block=" + ctx.blockDataSdk['hash'])


@given("that a block is returned by height {height} via the sdk")
def step_impl(ctx, height):
    print("that a block is returned by height {height} via the sdk")

    ctx.blockDataSdk = ctx.sdk_client.get_block()
    ctx.blockDataSdk = ctx.sdk_client.get_block(ctx.blockDataSdk['header']["height"])


@then("request the returned block from the test node via its hash")
def step_impl(ctx):
    print("request the returned block from the test node via its hash")
    ctx.blockDataNode = ctx.nctl_client.get_latest_block_by_param("block=" + ctx.blockDataSdk['hash'])


@given("that an invalid block hash is requested via the sdk")
def step_impl(ctx):
    print("that an invalid block hash is requested via the sdk")
    try:
        ctx.blockDataSdk = ctx.sdk_client.get_block(INVALID_BLOCK_HASH)
    except Exception as ex:
        ctx.exception = ex


@then("a valid error message is returned")
def step_impl(ctx):
    print("a valid error message is returned")

    assert type(ctx.exception) is NodeAPIError
    assert BLOCK_ERR_MSG == ctx.exception.args[0].message
    assert BLOCK_ERR_CODE == ctx.exception.args[0].code


@given("that an invalid block height is requested via the sdk")
def step_impl(ctx):
    print("that an invalid block height is requested via the sdk")

    try:
        ctx.blockDataSdk = ctx.sdk_client.get_block(INVALID_HEIGHT)
    except Exception as ex:
        ctx.exception = ex


@given("that a step event is received")
def step_impl(ctx):
    print("that a step event is received")

    call_async_function(ctx, step_event)
    ctx.nodeEraSwitchBlockData = ctx.nctl_client.get_era_switch_block()

    assert ctx.nodeEraSwitchBlockData['era_summary']
    assert ctx.nodeEraSwitchBlockData['era_summary']['block_hash']
    assert codecs.decode(ctx.nodeEraSwitchBlockData['era_summary']['block_hash'], 'hex')

    ctx.nodeEraSwitchBlock = ctx.nodeEraSwitchBlockData['era_summary']['block_hash']


@then("request the corresponding era switch block via the sdk")
def step_impl(ctx):
    print("request the corresponding era switch block via the sdk")

    ctx.eraSwitchBlockData = ctx.sdk_client.get_era_info(ctx.nodeEraSwitchBlock)
    assert ctx.eraSwitchBlockData


@step(
    "the switch block hashes of the returned block are equal to the switch block hashes of the returned test node block")
def step_impl(ctx):
    print("the switch block hashes of the returned block are equal to the switch block hashes of the returned test "
          "node block")

    assert ctx.nodeEraSwitchBlock == ctx.eraSwitchBlockData['block_hash']


@step("the switch block eras of the returned block are equal to the switch block eras of the returned test node block")
def step_impl(ctx):
    print("the switch block eras of the returned block are equal to the switch block eras of the returned test node "
          "block")

    ctx.nodeEraSwitchBlockData['era_summary']['era_id'] = ctx.eraSwitchBlockData['era_id']


@step(
    "the switch block merkle proofs of the returned block are equal to the switch block merkle proofs of the returned "
    "test node block")
def step_impl(ctx):
    print("the switch block merkle proofs of the returned block are equal to the switch block merkle proofs of the "
          "returned test node block")

    validate_merkle_proofs(ctx.nodeEraSwitchBlockData['era_summary']['merkle_proof'],
                           ctx.eraSwitchBlockData['merkle_proof'])


@step(
    "the switch block state root hashes of the returned block are equal to the switch block state root hashes of the "
    "returned test node block")
def step_impl(ctx):
    print("the switch block state root hashes of the returned block are equal to the switch block state root hashes "
          "of the returned test node block")

    assert ctx.nodeEraSwitchBlockData['era_summary']['state_root_hash'] == ctx.eraSwitchBlockData['state_root_hash']


@step("the delegators data of the returned block is equal to the delegators data of the returned test node block")
def step_impl(ctx):
    print("the delegators data of the returned block is equal to the delegators data of the returned test node block")

    assert ctx.nodeEraSwitchBlockData['era_summary']['stored_value']['EraInfo']['seigniorage_allocations'] \
           == ctx.eraSwitchBlockData['stored_value']['EraInfo']['seigniorage_allocations']


@step("the validators data of the returned block is equal to the validators data of the returned test node block")
def step_impl(ctx):
    print("the validators data of the returned block is equal to the validators data of the returned test node block")

    assert ctx.nodeEraSwitchBlockData['era_summary']['stored_value']['EraInfo']['seigniorage_allocations'] \
           == ctx.eraSwitchBlockData['stored_value']['EraInfo']['seigniorage_allocations']


@given("that chain transfer data is initialised")
def step_impl(ctx):
    print("that chain transfer data is initialised")

    ctx.sender_key = pycspr.parse_private_key(
        get_user_asset_path(ctx.ASSETS_ROOT, "1", "1", "secret_key.pem"),
        KeyAlgorithm.ED25519.name,
    )
    ctx.receiver_key = pycspr.parse_public_key(
        get_user_asset_path(ctx.ASSETS_ROOT, "1", "2", "public_key_hex")
    )

    ctx.transfer_amount = 2500000000
    ctx.gas_price = 1
    ctx.ttl = '30m'


@when("the deploy data is put on chain")
def step_impl(ctx):
    print("the deploy data is put on chain")

    deploy: Deploy

    deploy_params = pycspr.create_deploy_parameters(
        account=ctx.sender_key,
        chain_name='casper-net-1'
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


@then("the deploy response contains a valid deploy hash")
def step_impl(ctx):
    print("the deploy response contains a valid deploy hash")

    assert ctx.deploy_result
    assert ctx.deploy_result.hash.hex


@then("request the block transfer")
def step_impl(ctx):
    print("request the block transfer")

    ctx.transfer_block_sdk = call_async_function(ctx, block_event)


@then("request the block transfer from the test node")
def step_impl(ctx):
    print("request the block transfer from the test node")

    ctx.block_data_node = ctx.nctl_client.get_latest_block_by_param(
        "block=" + ctx.transfer_block_sdk['BlockAdded']['block_hash'])


@step("the returned block contains the transfer hash returned from the test node block")
def step_impl(ctx):
    print("the returned block contains the transfer hash returned from the test node block")

    assert ctx.deploy_result.hash.hex() in ctx.transfer_block_sdk['BlockAdded']['block']['body']['transfer_hashes']
