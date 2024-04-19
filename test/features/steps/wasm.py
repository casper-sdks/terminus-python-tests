import io
import os
import pathlib
import typing

import pycspr
from behave import *
from pycspr import parse_public_key_bytes, KeyAlgorithm, PrivateKey, PublicKey
from pycspr.crypto import get_key_pair
from pycspr.types.cl import *
from pycspr.types.node.rpc import *
from totaltimeout import Timeout

from test.features.steps.utils.assets import get_faucet_private_key

use_step_matcher("re")


# Step definitions for the wasm.feature

@given('that a smart contract "(.*)" is located in the "(.*)" folder')
def that_a_smart_contract_exists(ctx, file, location):
    print(f'that a smart contract "{file}" is located in the "{location}" folder')

    ctx.wasm_path = pathlib.Path(os.path.dirname(__file__)) / location / file
    ctx.wasm_stream = io.open(ctx.wasm_path, 'rb')

    assert ctx.wasm_stream


@when("the wasm is loaded as from the file system")
def step_impl(ctx):
    print('when the wasm is loaded as from the file system')

    _bytes = ctx.wasm_stream.read()
    assert len(_bytes) == 189336

    get_faucet_private_key(ctx)

    params: DeployParameters = \
        pycspr.create_deploy_parameters(
            account=ctx.sender_key,
            chain_name=ctx.chain_name
        )

    payment: DeployOfModuleBytes = \
        pycspr.create_standard_payment(200000000000)

    session: DeployOfModuleBytes = DeployOfModuleBytes(
        module_bytes=pycspr.read_wasm(ctx.wasm_path),
        args={
            "token_decimals": CLV_U8(11),
            "token_name": CLV_String('Acme Token'),
            "token_symbol": CLV_String('ACME'),
            "token_total_supply": CLV_U256(500000000000),
        }
    )

    deploy: Deploy = pycspr.create_deploy(params, payment, session)

    deploy.approve(ctx.sender_key)
    ctx.deploy_hash = ctx.sdk_client_rpc.send_deploy(deploy)

    assert ctx.deploy_hash
    print(ctx.deploy_hash)



@step("the wasm has been successfully deployed")
def the_wasm_has_been_successfully_deployed(ctx):
    print('when the wasm has been successfully deployed')

    deploy = wait_for_deploy(ctx)

    assert len(deploy) > 0


@then('the account named keys contain the "(.*)" name')
def the_account_named_keys_contain_the(ctx, contract_name):
    print(f'then the account named keys contain the {contract_name} name')

    faucet_private_key: PrivateKey = ctx.sender_key

    faucet_public_key = faucet_private_key.public_key
    account_hash = faucet_private_key.account_hash

    key = "account-hash-{}".format(account_hash.hex())
    account = ctx.sdk_client_rpc.get_state_item(key)

    assert account['Account']['named_keys'][0]['name'] == contract_name.upper()
    assert account['Account']['named_keys'][0]['key']
    ctx.contract_hash = account['Account']['named_keys'][0]['key']


@step('the contract data "(.*)" is a "(.*)" with a value of "(.*)" and bytes of "(.*)"')
def the_contract_data_is_a_with_a_value_of(ctx, path, type_name, value, hex_bytes):
    print(f'the contract data "{path}" is a "{type_name}" with a value of "{value}" and bytes of "{hex_bytes}"')

    state_item = ctx.sdk_client_rpc.get_state_item(
        ctx.contract_hash,
        [path]
    )

    assert state_item
    assert state_item['CLValue']['cl_type'] == type_name
    assert state_item['CLValue']['parsed'] == convert_value(type_name, value)
    assert state_item['CLValue']['bytes'] == hex_bytes


@then("the contract invocation deploy is successful")
def the_contract_invocation_deploy_is_successful(ctx):
    print('then the contract invocation deploy is successful')

    deploy = wait_for_deploy(ctx)
    assert len(deploy.execution_info) > 0


@when('the the contract is invoked by name "(.*)" and a transfer amount of "(.*)"')
def the_contract_is_invoked_by_name(ctx, name, amount):
    print(f'the the contract is invoked by name "{name}" and a transfer amount of "{amount}"')

    recipient_key_pair: typing.Union[bytes, bytes] = get_key_pair(algo=KeyAlgorithm["ED25519"])

    pvk, pbk = recipient_key_pair

    recipient_pk: PublicKey = parse_public_key_bytes(pbk, algo=KeyAlgorithm["ED25519"])

    get_faucet_private_key(ctx)

    params: DeployParameters = \
        pycspr.create_deploy_parameters(
            account=ctx.sender_key,
            chain_name=ctx.chain_name
        )

    # Set payment logic.
    payment: DeployOfModuleBytes = pycspr.create_standard_payment(2500000000)

    # Set session logic.
    session: DeployOfStoredContractByName = DeployOfStoredContractByName(
        entry_point="transfer",
        name=str(name).upper(),
        args={
            "amount": CLV_U256(int(amount)),
            "recipient": CLV_ByteArray(recipient_pk.account_hash)
        }
    )

    deploy: Deploy = pycspr.create_deploy(params, payment, session)

    assert deploy

    deploy.approve(ctx.sender_key)

    ctx.deploy_hash = ctx.sdk_client_rpc.send_deploy(deploy)

    assert ctx.deploy_hash


@when('the the contract is invoked by hash and version with a transfer amount of "(.*)"')
def the_contract_is_invoked_by_hash(ctx, amount):
    print(f'the the contract is invoked by hash and version with a transfer amount of "{amount}"')

    recipient_key_pair: typing.Union[bytes, bytes] = get_key_pair(algo=KeyAlgorithm["ED25519"])

    pvk, pbk = recipient_key_pair

    recipient_pk: PublicKey = parse_public_key_bytes(pbk, algo=KeyAlgorithm["ED25519"])

    get_faucet_private_key(ctx)

    params: DeployParameters = \
        pycspr.create_deploy_parameters(
            account=ctx.sender_key,
            chain_name=ctx.chain_name
        )

    # Set payment logic.
    payment: DeployOfModuleBytes = pycspr.create_standard_payment(2500000000)

    # Set session logic.
    session: DeployOfStoredContractByHashVersioned = DeployOfStoredContractByHashVersioned(
        entry_point="transfer",
        version=1,
        hash=bytes.fromhex(ctx.contract_hash[5:]),
        args={
            "amount": CLV_U256(int(amount)),
            "recipient": CLV_ByteArray(recipient_pk.account_hash)
        }
    )

    deploy: Deploy = pycspr.create_deploy(params, payment, session)

    assert deploy

    deploy.approve(ctx.sender_key)

    ctx.deploy_hash = ctx.sdk_client_rpc.send_deploy(deploy)

    assert ctx.deploy_hash


@when('the the contract is invoked by name "(.*)" and version with a transfer amount of "(.*)"')
def the_contract_is_invoked_by_name_and_version(ctx, name, amount):
    print(f'the the contract is invoked by name "{name}" and version with a transfer amount of "{amount}"')

    recipient_key_pair: typing.Union[bytes, bytes] = get_key_pair(algo=KeyAlgorithm["ED25519"])

    pvk, pbk = recipient_key_pair

    recipient_pk: PublicKey = parse_public_key_bytes(pbk, algo=KeyAlgorithm["ED25519"])

    get_faucet_private_key(ctx)

    params: DeployParameters = \
        pycspr.create_deploy_parameters(
            account=ctx.sender_key,
            chain_name=ctx.chain_name
        )

    # Set payment logic.
    payment: DeployOfModuleBytes = pycspr.create_standard_payment(2500000000)

    # Set session logic.
    session: DeployOfStoredContractByHashVersioned = DeployOfStoredContractByHashVersioned(
        entry_point="transfer",
        version=1,
        name=str(name).upper(),
        args={
            "amount": CLV_U256(int(amount)),
            "recipient": CLV_ByteArray(recipient_pk.account_hash)
        }
    )

    deploy: Deploy = pycspr.create_deploy(params, payment, session)

    assert deploy

    deploy.approve(ctx.sender_key)

    ctx.deploy_hash = ctx.sdk_client_rpc.send_deploy(deploy)

    assert ctx.deploy_hash


def convert_value(type_name, value):
    if type_name == "U8":
        return int(value)
    else:
        return value


def wait_for_deploy(ctx) -> dict:
    deploy: dict = None

    timeout = Timeout(300)

    deployed = False

    for t in timeout:
        deploy = ctx.sdk_client_rpc.get_deploy(ctx.deploy_hash)
        if deploy is not None and len(deploy.execution_info) > 0:
            deployed = True
            break

    assert deployed

    return deploy


@when('the contract entry point is invoked by hash with a transfer amount of "(.*)"')
def step_impl(ctx, amount):
    print(f'given the contract entry point is invoked with a transfer amount of "{amount}"')

    recipient_key_pair: typing.Union[bytes, bytes] = get_key_pair(algo=KeyAlgorithm["ED25519"])

    pvk, pbk = recipient_key_pair

    recipient_pk: PublicKey = parse_public_key_bytes(pbk, algo=KeyAlgorithm["ED25519"])

    get_faucet_private_key(ctx)

    params: DeployParameters = \
        pycspr.create_deploy_parameters(
            account=ctx.sender_key,
            chain_name=ctx.chain_name
        )

    # Set payment logic.
    payment: DeployOfModuleBytes = pycspr.create_standard_payment(2500000000)

    # Set session logic.
    session: DeployOfStoredContractByHash = DeployOfStoredContractByHash(
        entry_point="transfer",
        hash=bytes.fromhex(ctx.contract_hash[5:]),
        args={
            "amount": CLV_U256(int(amount)),
            "recipient": CLV_ByteArray(recipient_pk.account_hash)
        }
    )

    deploy: Deploy = pycspr.create_deploy(params, payment, session)

    assert deploy

    deploy.approve(ctx.sender_key)

    ctx.deploy_hash = ctx.sdk_client_rpc.send_deploy(deploy)

    assert ctx.deploy_hash
