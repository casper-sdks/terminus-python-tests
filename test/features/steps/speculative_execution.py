from behave import *

from pycspr.types.deploys import Deploy

use_step_matcher("re")
from utils.deploy import *

# Step Definitions for Speculative Execution Cucumber Tests

@given(
    'that the "(.*)" account transfers (.*) to user-(.*) account with a gas payment amount of (.*) using the speculative_exec RPC API')
def that_the_account_transfers_to_user(ctx, account, transfer_amount, user, payment_amount):
    print(
        f'that the "{account}" account transfers {transfer_amount} to user-{user} account with a gas payment amount of {payment_amount} using the speculative_exec RPC API')

    deploy: Deploy

    ctx.user = user

    deploy_set_faucet_key(ctx)
    deploy_set_receiver_key(ctx)

    deploy_params = pycspr.create_deploy_parameters(
        account=ctx.sender_key,
        chain_name=ctx.chain_name,
        ttl='30m',
        gas_price=1,
    )

    # Set deploy.
    deploy = pycspr.create_transfer(
        params=deploy_params,
        amount=int(transfer_amount),
        target=ctx.receiver_key.account_key,
        correlation_id=random.randint(1, 1e6),
        payment=int(payment_amount)
    )

    deploy.approve(ctx.sender_key)
    ctx.deploy = deploy

    ctx.deploy_result = ctx.sdk_client_spec.speculative_exec(deploy)

    assert ctx.deploy_result


@then('the speculative_exec has an api_version of "(.*)"')
def has_api_version(ctx, api):
    print(f'the speculative_exec has an api_version of "{api}"')

    assert ctx.deploy_result['api_version'] == api


@step("a valid speculative_exec_result will be returned with (.*) transforms")
def has_correct_amount_transforms(ctx, transforms):
    print(f'a valid speculative_exec_result will be returned with {transforms} transforms')

    assert len(ctx.deploy_result['execution_result']['Success']['effect']['transforms']) == int(transforms)


@step("the speculative_exec has a valid block_hash")
def has_valid_block_hash(ctx):
    print(f'the speculative_exec has a valid block_hash')

    assert len(ctx.deploy_result['block_hash']) == 64


@step("the execution_results contains a cost of (.*)")
def has_result_of_cost(ctx, cost):
    print(f'the execution_results contains a cost of {cost}')

    assert ctx.deploy_result['execution_result']['Success']['cost'] == cost


@step("the speculative_exec has a valid execution_result")
def has_valid_execution_result(ctx):
    print(f'the speculative_exec has a valid execution_result')

    get_write_transform(ctx)
    assert ctx.write_transform is not None


@step("the speculative_exec execution_result transform wth the transfer key contains the deploy_hash")
def execution_result_contains_the_deploy_hash(ctx):
    print(f'the speculative_exec execution_result transform wth the transfer key contains the deploy_hash')

    assert ctx.write_transform['transform']['WriteTransfer']['deploy_hash'] == ctx.deploy.hash.hex()


@step("the speculative_exec execution_result transform with the transfer key has the amount of (.*)")
def has_amount_of(ctx, transfer_amount):
    print(f'the speculative_exec execution_result transform with the transfer key has the amount of {transfer_amount}')

    assert ctx.write_transform['transform']['WriteTransfer']['amount'] == transfer_amount


@step(
    'the speculative_exec execution_result transform with the transfer key has the "(.*)" field set to the "(.*)" account hash')
def has_transfer_key_account_1(ctx, field_value, account):
    print(
        f'the speculative_exec execution_result transform with the transfer key has the "{field_value}" field set to the "{account}" account hash')

    if account == 'faucet':
        account_hash = ctx.sender_key.account_hash.hex()
    else:
        account_hash = ctx.receiver_key.account_hash.hex()

    assert account_hash in ctx.write_transform['transform']['WriteTransfer'][field_value]


@step(
    'the speculative_exec execution_result transform with the transfer key has the "(.*)" field set to the purse uref of the "(.*)" account')
def has_transfer_key_account_3(ctx, field_value, account):
    print(
        f'the speculative_exec execution_result transform with the transfer key has the "{field_value}" field set to the purse uref of the "{account}" account')

    if account == 'faucet':
        main_purse = ctx.sdk_client.get_account_info(ctx.sender_key.account_key)['main_purse'][0:-4]
    else:
        main_purse = ctx.sdk_client.get_account_info(ctx.receiver_key.account_key)['main_purse'][0:-4]

    assert main_purse in ctx.write_transform['transform']['WriteTransfer'][field_value]


@step("the speculative_exec execution_result transform with the deploy key has the deploy_hash of the transfer's hash")
def has_deploy_hash_of_transfer_hash(ctx):
    print(
        f"the speculative_exec execution_result transform with the deploy key has the deploy_hash of the transfer's hash")

    get_deploy_transform(ctx)

    assert ctx.deploy_transforms['transform']['WriteDeployInfo']['deploy_hash'] == ctx.deploy.hash.hex()


@step("the speculative_exec execution_result transform with a deploy key has a gas field of (.*)")
def has_a_gas_amount_of(ctx, gas):
    print(f'the speculative_exec execution_result transform with a deploy key has a gas field of {gas}')

    assert ctx.deploy_transforms['transform']['WriteDeployInfo']['gas'] == gas


@step("the speculative_exec execution_result transform with a deploy key has (.*) transfer with a valid transfer hash")
def has_n_transfers(ctx, transform):
    print(
        f'the speculative_exec execution_result transform with a deploy key has {transform} transfer with a valid transfer hash')

    assert len(ctx.deploy_transforms['transform']['WriteDeployInfo']['transfers']) == int(transform)
    assert len(ctx.deploy_transforms['transform']['WriteDeployInfo']['transfers'][0]) == 73


@step(
    'the speculative_exec execution_result transform with a deploy key has as from field of the "(.*)" account hash')
def has_from_account(ctx, account):
    print(
        f'the speculative_exec execution_result transform with a deploy key has as from field of the "{account}" account hash')

    assert ctx.sender_key.account_hash.hex() in ctx.deploy_transforms['transform']['WriteDeployInfo']['from']


@step(
    'the speculative_exec execution_result transform with a deploy key has as source field of the "(.*)" account purse uref')
def has_source_account(ctx, account):
    print(
        f'the speculative_exec execution_result transform with a deploy key has as source field of the "{account}" account purse uref')

    main_purse = ctx.sdk_client.get_account_info(ctx.sender_key.account_key)['main_purse']

    assert ctx.deploy_transforms['transform']['WriteDeployInfo']['source'] == main_purse


@step("the speculative_exec execution_result contains at least (.*) valid balance transforms")
def has_n_valid_balance_transforms(ctx, count):
    print(
        f'the speculative_exec execution_result contains at least {count} valid balance transforms')

    get_balance_transforms(ctx)

    assert len(ctx.balance_transform) >= int(count)


@step("the speculative_exec execution_result (.*)st balance transform is an Identity transform")
def has_identity_transform(ctx, index):
    print(
        f'the speculative_exec execution_result {index}st balance transform is an Identity transform')

    assert ctx.deploy_result['execution_result']['Success']['effect']['transforms'][ctx.balance_transform[int(index) - 1]][
        'transform'] == 'Identity'


@step(
    'the speculative_exec execution_result last balance transform is an Identity transform is as WriteCLValue of type "(.*)"')
def has_identity_of_type(ctx, type):
    print(
        f'the speculative_exec execution_result last balance transform is an Identity transform is as WriteCLValue of type "{type}"')

    transform = ctx.deploy_result['execution_result']['Success']['effect']['transforms'][ctx.balance_transform[-1]][
        'transform']

    assert transform['WriteCLValue']
    assert transform['WriteCLValue']['cl_type'] == type
    assert int(transform['WriteCLValue']['parsed']) > 99999


@step("the speculative_exec execution_result contains a valid (.*) transform with a value of (.*)")
def contains_valid_type(ctx, _type, value):
    print(
        f'the speculative_exec execution_result contains a valid {_type} transform with a value of {value}')

    transform = ctx.deploy_result['execution_result']['Success']['effect']['transforms'][-1]['transform']

    assert transform[_type]
    assert transform[_type] == value


@step("the speculative_exec execution_result contains a valid balance transform")
def contains_a_valid_transform(ctx):
    print(
        f'the speculative_exec execution_result contains a valid balance transform')

    transform = ctx.deploy_result['execution_result']['Success']['effect']['transforms'][ctx.balance_transform[0]]

    assert transform
    assert 'balance-' in transform['key']


def deploy_set_receiver_key(ctx):
    ctx.receiver_key = pycspr.parse_public_key(
        ctx.get_user_asset_path(ctx.ASSETS_ROOT, "1", 'user-{}'.format(ctx.user), "public_key_hex")
    )


def get_deploy_transform(ctx):
    key = f'deploy-{ctx.deploy.hash.hex()}'
    ctx.deploy_transforms = next(
        (x for x in ctx.deploy_result['execution_result']['Success']['effect']['transforms'] if x['key'] == key), None)

    assert ctx.deploy_transforms is not None


def get_balance_transforms(ctx):
    main_purse = ctx.sdk_client.get_account_info(ctx.sender_key.account_key)['main_purse'][5:-4]
    ctx.balance_transform = [i for i, x in
                             enumerate(ctx.deploy_result['execution_result']['Success']['effect']['transforms']) if
                             x['key'] == f'balance-{main_purse}']

    assert len(ctx.balance_transform) > 0


def get_write_transform(ctx):
    key = ctx.deploy_result['execution_result']['Success']['transfers'][0]
    ctx.write_transform = next(
        (x for x in ctx.deploy_result['execution_result']['Success']['effect']['transforms'] if x['key'] == key), None)
