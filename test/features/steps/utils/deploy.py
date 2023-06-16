import random

import pycspr
from pycspr import KeyAlgorithm
from pycspr.types import Deploy


def deploy_to_chain(ctx) -> Deploy:
    deploy: Deploy

    # deploy_get_signatures(ctx)

    deploy_params = pycspr.create_deploy_parameters(
        account=ctx.sender_key,
        chain_name=ctx.chain,
        ttl=ctx.ttl,
        gas_price=ctx.gas_price
    )

    # Set deploy.
    deploy = pycspr.create_transfer(
        params=deploy_params,
        amount=int(ctx.transfer_amount),
        target=ctx.receiver_key.account_key,
        correlation_id=random.randint(1, 1e6),
        payment=int(ctx.payment_amount)
    )

    deploy.approve(ctx.sender_key)

    ctx.sdk_client.send_deploy(deploy)

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
