from behave import *


@given("that the latest block is requested via the sdk")
def step_impl(context):
    print("that the latest block is requested via the sdk")
    context.blockDataSdk = context.sdk_client.get_block()


@then('request the latest block via the test node')
def step_impl(context):
    print("request the latest block via the test node")
    context.blockDataNode = context.nctl_client.get_latest_block()


@then("the body of the returned block is equal to the body of the returned test node block")
def step_impl(context):
    print("the body of the returned block is equal to the body of the returned test node block")

    assert len(context.blockDataSdk['body']) > 0
    assert context.blockDataSdk['body']['proposer'] == context.blockDataNode['body']['proposer']
    assert context.blockDataSdk['body']['deploy_hashes'] == context.blockDataNode['body']['deploy_hashes']
    assert context.blockDataSdk['body']['transfer_hashes'] == context.blockDataNode['body']['transfer_hashes']


@step("the hash of the returned block is equal to the hash of the returned test node block")
def step_impl(context):
    print("the hash of the returned block is equal to the hash of the returned test node block")

    assert context.blockDataSdk['hash'] == context.blockDataNode['hash']


@step("the header of the returned block is equal to the header of the returned test node block")
def step_impl(context):
    print("the header of the returned block is equal to the header of the returned test node block")

    assert context.blockDataSdk['header'] == context.blockDataNode['header']


@step("the proofs of the returned block are equal to the proofs of the returned test node block")
def step_impl(context):
    print("the proofs of the returned block are equal to the proofs of the returned test node block")

    assert context.blockDataSdk['proofs'] == context.blockDataNode['proofs']


@given("that a block is returned by hash via the sdk")
def step_impl(context):
    context.blockDataSdk = context.sdk_client.get_block()
    context.blockDataSdk = context.sdk_client.get_block(context.blockDataSdk['hash'])


@then("request a block by hash via the test node")
def step_impl(context):
    context.blockDataNode = context.nctl_client.get_latest_block_by_param(context.blockDataSdk['hash'])
