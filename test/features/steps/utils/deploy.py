import random

import pycspr
import pycspr.types
from pycspr import KeyAlgorithm, types
from pycspr.types import Deploy, DeployParameters, ModuleBytes


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

def create_deploy(ctx):

    deploy: Deploy

    params: DeployParameters = \
        pycspr.create_deploy_parameters(
            account=ctx.sender_key,
            chain_name=ctx.chain
            )

    # arg = DeployArgument("an-argument", cl_value)

    payment: ModuleBytes = \
        pycspr.create_standard_payment(ctx.payment_amount)

    args: dict = {}
    for arg in ctx.deploy_args:
        for key, value in arg.items():
            args.update({key: value})



    session: ModuleBytes = ModuleBytes(
        module_bytes=pycspr.read_wasm(ctx.wasm_path),
        args={
                "amount": types.CL_U512(2500000000),
                "target": types.CL_PublicKey(KeyAlgorithm.ED25519, ctx.receiver_key.account_hash),
                "id": pycspr.types.CL_Option(pycspr.types.CL_U64(200), pycspr.types.CL_U64).value,
                "option": types.CL_Option(types.CL_Bool(True), types.CL_Bool).value,
                "tuple1": types.CL_Tuple1(types.CL_String('ACME')),
                "tuple2": types.CL_Tuple2(types.CL_String('ACME'), types.CL_U32(10000)),
                "tuple3": types.CL_Tuple3(types.CL_String('ACME'), types.CL_U32(10000), types.CL_Bool(False)),
                "list": types.CL_List([types.CL_String('Alpha'), types.CL_String('Beta'),  types.CL_String('Delta'),
                                       types.CL_String('Gamma'),  types.CL_String('Epsilon'), ])
            }
    )

    deploy = pycspr.create_deploy(params, payment, session)

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
