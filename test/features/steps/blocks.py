import codecs

import pycspr.api.rest.proxy
from behave import *


from test.features.steps.utils.deploy import deploy_to_chain, deploy_set_signatures
from utils.assets import *
from utils.asyncs import *
from utils.validate import *

# Step Definitions for Block Cucumber Tests


INVALID_BLOCK_HASH = "2fe9630b7790852e4409d815b04ca98f37effcdf9097d317b9b9b8ad658f47c8"
INVALID_HEIGHT = 9999999999
BLOCK_ERR_MSG = "No such block"
BLOCK_ERR_CODE = -32001


@given("that the latest block is requested via the sdk")
def the_latest_block_returned(ctx):
    print("that the latest block is requested via the sdk")
    ctx.block_data_sdk = async_rpc_call(ctx.sdk_client_rpc.get_block())


@then('request the latest block via the test node')
def request_the_latest_block(ctx):
    print("request the latest block via the test node")
    ctx.block_data_node = ctx.node_client.get_latest_block()


@then("the body of the returned block is equal to the body of the returned test node block")
def returned_block_body_equal_to_test_node_returned_body(ctx):
    print("the body of the returned block is equal to the body of the returned test node block")

    if ctx.block_data_sdk.hash.hex() != ctx.block_data_node['hash']:
        # Fixes intermittent syncing issues with node/sdk latest blocks
        ctx.block_data_sdk = async_rpc_call(ctx.sdk_client_rpc.get_block(ctx.block_data_node['hash']))

    assert ctx.block_data_sdk.body.proposer.account_key.hex() == ctx.block_data_node['body']['proposer']
    assert ctx.block_data_sdk.body.deploy_hashes == ctx.block_data_node['body']['deploy_hashes']
    assert ctx.block_data_sdk.body.transfer_hashes == ctx.block_data_node['body']['transfer_hashes']


@step("the hash of the returned block is equal to the hash of the returned test node block")
def returned_block_hash_equal_to_returned_test_node_hash(ctx):
    print("the hash of the returned block is equal to the hash of the returned test node block")

    assert ctx.block_data_sdk.hash.hex() == ctx.block_data_node['hash']


@step("the header of the returned block is equal to the header of the returned test node block")
def returned_block_header_equal_to_returned_test_node_header(ctx):
    print("the header of the returned block is equal to the header of the returned test node block")

    assert ctx.block_data_sdk.header.accumulated_seed.hex() == ctx.block_data_node['header']['accumulated_seed']
    assert ctx.block_data_sdk.header.body_hash.hex() == ctx.block_data_node['header']['body_hash']
    assert ctx.block_data_sdk.header.era_end == ctx.block_data_node['header']['era_end']
    assert ctx.block_data_sdk.header.era_id == ctx.block_data_node['header']['era_id']
    assert ctx.block_data_sdk.header.height == ctx.block_data_node['header']['height']
    assert ctx.block_data_sdk.header.parent_hash.hex() == ctx.block_data_node['header']['parent_hash']

    assert (f'{ctx.block_data_sdk.header.protocol_version.major}.{ctx.block_data_sdk.header.protocol_version.minor}.'
            f'{ctx.block_data_sdk.header.protocol_version.revision}') == ctx.block_data_node['header']['protocol_version']

    assert ctx.block_data_sdk.header.random_bit == ctx.block_data_node['header']['random_bit']
    assert ctx.block_data_sdk.header.state_root.hex() == ctx.block_data_node['header']['state_root_hash']
    assert compare_dates(ctx.block_data_node['header']['timestamp'], ctx.block_data_sdk.header.timestamp)


@step("the proofs of the returned block are equal to the proofs of the returned test node block")
def returned_block_proofs_equal_to_returned_test_node_proofs(ctx):
    print("the proofs of the returned block are equal to the proofs of the returned test node block")

    for i in range(len(ctx.block_data_node['proofs'])):
        assert ctx.block_data_sdk.proofs[i].public_key.account_key.hex() == ctx.block_data_node['proofs'][i]['public_key']
        assert ctx.block_data_sdk.proofs[i].signature.as_bytes.hex() == ctx.block_data_node['proofs'][i]['signature']


@given("that a block is returned by hash via the sdk")
def a_block_returned_by_hash(ctx):
    ctx.block_data_sdk = async_rpc_call(ctx.sdk_client_rpc.get_block())
    ctx.block_data_sdk = async_rpc_call(ctx.sdk_client_rpc.get_block(ctx.block_data_sdk.hash))


@then("request a block by hash via the test node")
def request_block_by_hash_from_test_node(ctx):
    print("request a block by hash via the test node")

    ctx.block_data_node = ctx.node_client.get_latest_block_by_param(f'block={ctx.block_data_sdk.hash.hex()}')


@given("that a block is returned by height {height} via the sdk")
def a_block_is_returned_by_height(ctx, height):
    print("that a block is returned by height {height} via the sdk")

    ctx.block_data_sdk = async_rpc_call(ctx.sdk_client_rpc.get_block())
    ctx.block_data_sdk = async_rpc_call(ctx.sdk_client_rpc.get_block(ctx.block_data_sdk.header.height))


@then("request the returned block from the test node via its hash")
def a_block_is_returned_by_hash_from_test_node(ctx):
    print("request the returned block from the test node via its hash")
    ctx.block_data_node = ctx.node_client.get_latest_block_by_param(f'block={ctx.block_data_sdk.hash.hex()}')


@given("that an invalid block hash is requested via the sdk")
def an_invalid_block_is_requested(ctx):
    print("that an invalid block hash is requested via the sdk")
    try:
        ctx.block_data_sdk = async_rpc_call(ctx.sdk_client_rpc.get_block(INVALID_BLOCK_HASH))
    except Exception as ex:
        ctx.exception = ex


@then("a valid error message is returned")
def a_valid_error_message_is_returned(ctx):
    print("a valid error message is returned")

    # assert type(ctx.exception) is Exception
    assert BLOCK_ERR_MSG == ctx.exception.args[0].message
    assert BLOCK_ERR_CODE == ctx.exception.args[0].code


@given("that an invalid block height is requested via the sdk")
def an_invalid_block_height_is_requested(ctx):
    print("that an invalid block height is requested via the sdk")

    try:
        ctx.block_data_sdk = ctx.sdk_client_rpc.get_block(INVALID_HEIGHT)
    except Exception as ex:
        ctx.exception = ex


@given("that a step event is received")
def a_step_event_is_received(ctx):
    print("that a step event is received")

    call_async_function(ctx, step_event)
    ctx.node_era_switch_block_data = ctx.node_client.get_era_summary()

    assert ctx.node_era_switch_block_data['era_summary']
    assert ctx.node_era_switch_block_data['era_summary']['block_hash']
    assert codecs.decode(ctx.node_era_switch_block_data['era_summary']['block_hash'], 'hex')

    ctx.nodeEraSwitchBlock = ctx.node_era_switch_block_data['era_summary']['block_hash']


@then("request the corresponding era switch block via the sdk")
def request_corresponding_era_switch_block(ctx):
    print("request the corresponding era switch block via the sdk")

    ctx.eraSwitchBlockData = ctx.sdk_client_rpc.get_era_info(ctx.nodeEraSwitchBlock)
    assert ctx.eraSwitchBlockData


@step(
    "the switch block hashes of the returned block are equal to the switch block hashes of the returned test node block")
def switch_block_hashes_are_equal(ctx):
    print("the switch block hashes of the returned block are equal to the switch block hashes of the returned test "
          "node block")

    assert ctx.nodeEraSwitchBlock == ctx.eraSwitchBlockData['era_summary']['block_hash']


@step("the switch block eras of the returned block are equal to the switch block eras of the returned test node block")
def switch_block_eras_are_equal(ctx):
    print("the switch block eras of the returned block are equal to the switch block eras of the returned test node "
          "block")

    ctx.node_era_switch_block_data['era_summary']['era_id'] = ctx.eraSwitchBlockData['era_summary']['era_id']


@step(
    "the switch block merkle proofs of the returned block are equal to the switch block merkle proofs of the returned "
    "test node block")
def switch_block_merkle_proofs_are_equal(ctx):
    print("the switch block merkle proofs of the returned block are equal to the switch block merkle proofs of the "
          "returned test node block")

    validate_merkle_proofs(ctx.node_era_switch_block_data['era_summary']['merkle_proof'],
                           ctx.eraSwitchBlockData['era_summary']['merkle_proof'])


@step(
    "the switch block state root hashes of the returned block are equal to the switch block state root hashes of the "
    "returned test node block")
def switch_block_state_root_hashes_are_equal(ctx):
    print("the switch block state root hashes of the returned block are equal to the switch block state root hashes "
          "of the returned test node block")

    assert ctx.node_era_switch_block_data['era_summary']['state_root_hash'] == ctx.eraSwitchBlockData['era_summary']['state_root_hash']


@step("the delegators data of the returned block is equal to the delegators data of the returned test node block")
def the_delegators_are_equal(ctx):
    print("the delegators data of the returned block is equal to the delegators data of the returned test node block")

    assert ctx.node_era_switch_block_data['era_summary']['stored_value']['EraInfo']['seigniorage_allocations'] \
           == ctx.eraSwitchBlockData['era_summary']['stored_value']['EraInfo']['seigniorage_allocations']


@step("the validators data of the returned block is equal to the validators data of the returned test node block")
def the_validators_are_equal(ctx):
    print("the validators data of the returned block is equal to the validators data of the returned test node block")

    assert ctx.node_era_switch_block_data['era_summary']['stored_value']['EraInfo']['seigniorage_allocations'] \
           == ctx.eraSwitchBlockData['era_summary']['stored_value']['EraInfo']['seigniorage_allocations']


@given("that chain transfer data is initialised")
def chain_transfer_data_is_initialised(ctx):
    print("that chain transfer data is initialised")

    ctx.sender_key = pycspr.parse_private_key(
        get_user_asset_path(ctx.ASSETS_ROOT, "1", "user-1", "secret_key.pem"),
        KeyAlgorithm.ED25519.name,
    )
    ctx.receiver_key = pycspr.parse_public_key(
        get_user_asset_path(ctx.ASSETS_ROOT, "1", "user-2", "public_key_hex")
    )

    ctx.transfer_amount = 2500000000
    ctx.payment_amount = 10000
    ctx.gas_price = 1
    ctx.ttl = '30m'


@when("the deploy data is put on chain")
def a_deploy_is_put_on_chain(ctx):
    print("the deploy data is put on chain")

    deploy_set_signatures(ctx)
    ctx.deploy_result = deploy_to_chain(ctx)

    assert ctx.deploy_result


@then("the deploy response contains a valid deploy hash")
def the_deploy_response_has_valid_deploy_hash(ctx):
    print("the deploy response contains a valid deploy hash")

    assert ctx.deploy_result
    assert ctx.deploy_result.hash.hex


@then("request the block transfer")
def request_block_transfer(ctx):
    print("request the block transfer")
    ctx.timeout = int(300)
    ctx.last_block_added = call_async_function(ctx, block_event)

    ctx.transfer_block_sdk = async_rpc_call(ctx.sdk_client_rpc.get_block_transfers())


@then("request the block transfer from the test node")
def step_request_block_transfer_from_test_node(ctx):
    print("request the block transfer from the test node")

    ctx.block_data_node = ctx.node_client.get_latest_block_by_param(
        f'block={ctx.transfer_block_sdk.block_hash.hex()}')


@step("the returned block contains the transfer hash returned from the test node block")
def returned_block_hash_transfer_hash_from_test_node(ctx):
    print("the returned block contains the transfer hash returned from the test node block")

    assert ctx.deploy_result.hash.hex() in ctx.block_data_node['body']['transfer_hashes']
