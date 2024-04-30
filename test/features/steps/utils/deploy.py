import random

import pycspr
import pycspr.types
from pycspr.types.cl import *
from pycspr import KeyAlgorithm, create_deploy_arguments

from pycspr.types.node.rpc import Deploy, DeployParameters, Transfer, DeployArgument, DeployOfModuleBytes, DeployOfTransfer

from test.features.steps.utils.asyncs import async_rpc_call


def deploy_to_chain(ctx) -> Deploy:
    deploy: Deploy

    # deploy_get_signatures(ctx)

    deploy_params = pycspr.create_deploy_parameters(
        account=ctx.sender_key,
        chain_name=ctx.chain_name,
        ttl=ctx.ttl,
        gas_price=ctx.gas_price,
    )

    # Set deploy
    deploy = pycspr.create_transfer(
        params=deploy_params,
        amount=int(ctx.transfer_amount),
        target=ctx.receiver_key,
        correlation_id=random.randint(1, 100),
        payment=int(ctx.payment_amount)
    )

    deploy.approve(ctx.sender_key)

    async_rpc_call(ctx.sdk_client_rpc.send_deploy(deploy))

    return deploy


def create_deploy(ctx):
    deploy: Deploy

    params: DeployParameters = \
        pycspr.create_deploy_parameters(
            account=ctx.sender_key,
            chain_name=ctx.chain_name,
            ttl=ctx.ttl,
            gas_price=ctx.gas_price
        )

    payment: DeployOfModuleBytes = \
        pycspr.create_standard_payment(ctx.payment_amount)

    transfer: DeployOfTransfer = pycspr.factory.create_transfer_session(
        amount=2500000000,
        target=ctx.receiver_key,
        correlation_id=200)


    # _args = create_deploy_arguments(ctx.cl_values[0])
    _args = []
    for arg in range(len(ctx.cl_values)):
        _args.append(create_deploy_arguments(ctx.cl_values[arg]))
        # transfer.args.append(create_deploy_arguments(ctx.cl_values[arg]))

    transfer.args.update({k: v for x in ctx.cl_values for k, v in x.items()})

    deploy: Deploy = pycspr.create_deploy(params, payment, transfer)

    deploy.approve(ctx.sender_key)

    return deploy


def deploy_set_signatures(ctx):
    ctx.sender_key = pycspr.parse_private_key(
        ctx.get_user_asset_path(ctx.ASSETS_ROOT, "1", 'user-{}'.format(ctx.user_1), "secret_key.pem"),
        KeyAlgorithm.ED25519.name,
    )
    ctx.receiver_key = pycspr.parse_public_key(
        ctx.get_user_asset_path(ctx.ASSETS_ROOT, "1", 'user-{}'.format(ctx.user_2), "public_key_hex")
    )


def deploy_set_faucet_key(ctx):
    ctx.sender_key = pycspr.parse_private_key(
        ctx.get_user_asset_path(ctx.ASSETS_ROOT, "1", 'faucet', "secret_key.pem"),
        KeyAlgorithm.ED25519.name,
    )

