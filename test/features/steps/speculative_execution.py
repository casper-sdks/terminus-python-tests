from behave import *

use_step_matcher("re")


@given(
    'that the "(.*)" account transfers (.*) to user-(.*) account with a gas payment amount of (.*) using the speculative_exec RPC API')
def that_the_account_transfers_to_user(ctx, account, transfer_amount, user, payment_amount):
    print(f'that the "{account}" account transfers {transfer_amount} to user-{user} account with a gas payment amount of {payment_amount} using the speculative_exec RPC API')


@then('the speculative_exec has an api_version of "(.*)"')
def has_api_version(ctx, api):
    print(f'the speculative_exec has an api_version of "{api}"')


@step("a valid speculative_exec_result will be returned with (.*) transforms")
def has_correct_amount_transforms(ctx, transforms):
    print(f'a valid speculative_exec_result will be returned with {transforms} transforms')


@step("the speculative_exec has a valid block_hash")
def has_valid_block_hash(ctx):
    print(f'the speculative_exec has a valid block_hash')


@step("the execution_results contains a cost of (.*)")
def has_result_of_cost(ctx, cost):
    print(f'the execution_results contains a cost of {cost}')

@step("the speculative_exec has a valid execution_result")
def has_valid_execution_result(ctx):
    print(f'the speculative_exec has a valid execution_result')


@step("the speculative_exec execution_result transform wth the transfer key contains the deploy_hash")
def execution_result_contains_the_deploy_hash(ctx):
    print(f'the speculative_exec execution_result transform wth the transfer key contains the deploy_hash')


@step("the speculative_exec execution_result transform with the transfer key has the amount of (.*)")
def has_amount_of(ctx, transfer_amount):
    print(f'the speculative_exec execution_result transform with the transfer key has the amount of {transfer_amount}')


@step(
    'the speculative_exec execution_result transform with the transfer key has the "(.*)" field set to the "(.*)" account hash')
def has_transfer_key_account(ctx, field_value, account):
    print(f'the speculative_exec execution_result transform with the transfer key has the "{field_value}" field set to the "{account}" account hash')

@step(
    'the speculative_exec execution_result transform with the transfer key has the "(.*)" field set to the "(.*)" account hash')
def has_transfer_key_account(ctx, field_value, account):
    print(
        f'the speculative_exec execution_result transform with the transfer key has the "{field_value}" field set to the "{account}" account hash')


@step(
    'the speculative_exec execution_result transform with the transfer key has the "(.*)" field set to the purse uref of the "(.*)" account')
def has_transfer_key_account(ctx, field_value, account):
    print(
        f'the speculative_exec execution_result transform with the transfer key has the "{field_value}" field set to the purse uref of the "{account}" account')


@step(
    'the speculative_exec execution_result transform with the transfer key has the "(.*)" field set to the purse uref of the "(.*)" account')
def has_transfer_key_account(ctx, field_value, account):
    print(
        f'the speculative_exec execution_result transform with the transfer key has the "{field_value}" field set to the purse uref of the "{account}" account')


@step("the speculative_exec execution_result transform with the deploy key has the deploy_hash of the transfer's hash")
def has_deploy_hash_of_transfer_hash(ctx):
    print(f"the speculative_exec execution_result transform with the deploy key has the deploy_hash of the transfer's hash")


@step("the speculative_exec execution_result transform with a deploy key has a gas field of (.*)")
def has_a_gas_amount_of(ctx, gas):
    print(f'the speculative_exec execution_result transform with a deploy key has a gas field of {gas}')


@step("the speculative_exec execution_result transform with a deploy key has (.*) transfer with a valid transfer hash")
def has_n_transfers(ctx, transform):
    print(f'the speculative_exec execution_result transform with a deploy key has {transform} transfer with a valid transfer hash')


@step(
    'the speculative_exec execution_result transform with a deploy key has as from field of the "(.*)" account hash')
def has_from_account(ctx, account):
    print(f'the speculative_exec execution_result transform with a deploy key has as from field of the "{account}" account hash')


@step(
    'the speculative_exec execution_result transform with a deploy key has as source field of the "(.*)" account purse uref')
def has_source_account(ctx, account):
    print(f'the speculative_exec execution_result transform with a deploy key has as source field of the "{account}" account purse uref')


@step("the speculative_exec execution_result contains at least (.*) valid balance transforms")
def has_n_valid_balance_transforms(ctx, count):
    print(
        f'the speculative_exec execution_result contains at least {count} valid balance transforms')


@step("the speculative_exec execution_result (.*)st balance transform is an Identity transform")
def has_identity_transform(ctx, index):
    print(
        f'the speculative_exec execution_result {index}st balance transform is an Identity transform')


@step(
    'the speculative_exec execution_result last balance transform is an Identity transform is as WriteCLValue of type "(.*)"')
def has_identity_of_type(ctx, type):
    print(
        f'the speculative_exec execution_result last balance transform is an Identity transform is as WriteCLValue of type "{type}"')


@step("the speculative_exec execution_result contains a valid (.*) transform with a value of (.*)")
def contains_valid_type(ctx, _type, value):
    print(
        f'the speculative_exec execution_result contains a valid {_type} transform with a value of {value}')


@step("the speculative_exec execution_result contains a valid balance transform")
def contains_a_valid_transform(ctx):
    print(
        f'the speculative_exec execution_result contains a valid balance transform')
