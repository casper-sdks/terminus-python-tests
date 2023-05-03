from behave import *
from pycspr import *

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
    ctx.blockDataNode = ctx.nctl_client.get_latest_block_by_param("block=" + ctx.blockDataSdk['hash'])


@given("that a block is returned by height {height} via the sdk")
def step_impl(ctx, height):
    ctx.blockDataSdk = ctx.sdk_client.get_block()
    ctx.blockDataSdk = ctx.sdk_client.get_block(ctx.blockDataSdk['header']["height"])


@then("request the returned block from the test node via its hash")
def step_impl(ctx):
    ctx.blockDataNode = ctx.nctl_client.get_latest_block_by_param("block=" + ctx.blockDataSdk['hash'])


@given("that an invalid block hash is requested via the sdk")
def step_impl(ctx):
    try:
        ctx.blockDataSdk = ctx.sdk_client.get_block(INVALID_BLOCK_HASH)
    except Exception as ex:
        ctx.exception = ex


@then("a valid error message is returned")
def step_impl(ctx):
    assert type(ctx.exception) is NodeAPIError
    assert BLOCK_ERR_MSG == ctx.exception.args[0].message
    assert BLOCK_ERR_CODE == ctx.exception.args[0].code


@given("that an invalid block height is requested via the sdk")
def step_impl(ctx):
    try:
        ctx.blockDataSdk = ctx.sdk_client.get_block(INVALID_HEIGHT)
    except Exception as ex:
        ctx.exception = ex
