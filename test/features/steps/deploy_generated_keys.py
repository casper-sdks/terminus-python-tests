import typing

from behave import *
from pycspr import KeyAlgorithm, parse_public_key_bytes, parse_private_key_bytes
from pycspr.crypto import get_key_pair
from pycspr.types import PublicKey, PrivateKey

from test.features.steps.utils.deploy import deploy_to_chain, deploy_set_faucet_key

use_step_matcher("re")

# Step Definitions for Deploys Cucumber Tests with generated keys


@given('that a "(.*)" sender key is generated')
def step_impl(ctx, algo):
    print('that a {} sender keys is generated'.format(algo))

    # Create new key pair.
    key_pair: typing.Union[bytes, bytes] = get_key_pair(algo=KeyAlgorithm[algo.upper()])

    assert len(key_pair) == 2

    pvk, pbk = key_pair
    assert isinstance(pvk, bytes) and isinstance(pbk, bytes)

    pk: PublicKey = parse_private_key_bytes(pvk, algo=KeyAlgorithm[algo.upper()])
    assert pk

    sk: PrivateKey = parse_private_key_bytes(pvk, algo=KeyAlgorithm[algo.upper()])
    assert sk

    ctx.sender_key_generated = sk
    ctx.receiver_key_generated = pk


@given('that a "(.*)" receiver key is generated')
def step_impl(ctx, algo):
    print('that a "{}" receiver key is generated'.format(algo))

    key_pair: typing.Union[bytes, bytes] = get_key_pair(algo=KeyAlgorithm[algo.upper()])

    assert len(key_pair) == 2

    pvk, pbk = key_pair
    assert isinstance(pvk, bytes) and isinstance(pbk, bytes)

    pk: PublicKey = parse_public_key_bytes(pbk, algo=KeyAlgorithm[algo.upper()])
    assert pk

    ctx.receiver_key_generated = pk


@then("fund the account from the faucet user with a transfer amount of (.*) and a payment amount of (.*)")
def step_impl(ctx, transfer_amount, payment_amount):

    print('fund the account from the faucet user with a transfer amount of {} and a payment amount of {}'
          .format(transfer_amount, payment_amount))

    ctx.transfer_amount = transfer_amount
    ctx.gas_price = 1
    ctx.ttl = '30m'
    ctx.chain = 'cspr-dev-cctl'
    ctx.payment_amount = payment_amount

    deploy_set_faucet_key(ctx)
    ctx.receiver_key = ctx.receiver_key_generated
    ctx.deploy_result = deploy_to_chain(ctx)

    assert ctx.deploy_result


@then("transfer to the receiver account the transfer amount of (.*) and the payment amount of (.*)")
def step_impl(ctx, transfer_amount, payment_amount):

    print('transfer to the receiver account the transfer amount of {} and the payment amount of {}'
          .format(transfer_amount, payment_amount))

    ctx.transfer_amount = transfer_amount
    ctx.sender_key = ctx.sender_key_generated
    ctx.receiver_key = ctx.receiver_key_generated
    ctx.payment_amount = payment_amount

    ctx.deploy_result = deploy_to_chain(ctx)

    assert ctx.deploy_result


@step('the returned block header proposer contains the "(.*)" algo')
def step_impl(ctx, algo):
    print('the returned block header proposer contains the "{}" algo'.format(algo))

    assert ctx.deploy_result.session.args['target'].algo.name == algo.upper()
