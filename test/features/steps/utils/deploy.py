import random

import pycspr
from pycspr import KeyAlgorithm
from pycspr.types import Deploy


def deploy_to_chain(ctx) -> Deploy:
    deploy: Deploy

    _get_counter_parties(ctx)

    deploy_params = pycspr.create_deploy_parameters(
        account=ctx.sender_key,
        chain_name=ctx.chain,
        ttl=ctx.ttl,
        gas_price=ctx.gas_price
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

    return deploy


def _get_counter_parties(ctx):
    ctx.sender_key = pycspr.parse_private_key(
        ctx.get_user_asset_path(ctx.ASSETS_ROOT, "1", ctx.user_1, "secret_key.pem"),
        KeyAlgorithm.ED25519.name,
    )
    ctx.receiver_key = pycspr.parse_public_key(
        ctx.get_user_asset_path(ctx.ASSETS_ROOT, "1", ctx.user_2, "public_key_hex")
    )
