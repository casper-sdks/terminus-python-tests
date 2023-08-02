import random

import pycspr
import pycspr.types
from pycspr import KeyAlgorithm
from pycspr.types import Deploy, DeployParameters, ModuleBytes, Transfer


def deploy_to_chain(ctx) -> Deploy:
    deploy: Deploy

    # deploy_get_signatures(ctx)

    deploy_params = pycspr.create_deploy_parameters(
        account=ctx.sender_key,
        chain_name=ctx.chain,
        ttl=ctx.ttl,
        gas_price=ctx.gas_price,
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
            chain_name=ctx.chain,
            ttl=ctx.ttl,
            gas_price=ctx.gas_price,
        )

    payment: ModuleBytes = \
        pycspr.create_standard_payment(ctx.payment_amount)

    args: dict = {}
    for arg in ctx.deploy_args:
        for key, value in arg.items():
            args.update({key: value})

    transfer: Transfer = pycspr.factory.create_transfer_session(2500000000, ctx.receiver_key.account_key, 200)
    transfer.args.update(args)

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



    # transfer.args.update({"ByteArray": types.CL_ByteArray(bytes.fromhex('01ec7ff7b401fd62efa877b0a88295928fc1ecd93fd3cc6d58373dd38f098724be'))})
    # transfer.args.update({"PublicKey": types.CL_PublicKey.from_account_key(bytes.fromhex('01ee5c4b8fed1d3b9ad0c4e491d3d5fe2b4a9d9cf04c6fc429c2da4e619a449919'))})
    # transfer.args.update({"Key": types.CL_Key.from_string(('account-hash-016ff3127d815871618b6f639cf4a4a2df4edeacb8a0df662822707a5e570c9d32'))})
    # transfer.args.update({"Tuple1": types.CL_Tuple1(types.CL_String('ACME'))})
    # transfer.args.update({"Option": types.CL_Option(types.CL_Bool(True), types.CL_Bool).value})
    # transfer.args.update({"Tuple2": types.CL_Tuple2(types.CL_String('ACME'), types.CL_U32(10000))})
    # transfer.args.update({"Tuple3": types.CL_Tuple3(types.CL_String('ACME'), types.CL_U32(10000), types.CL_Bool(False))})
    # transfer.args.update({"List": types.CL_List([types.CL_String('Alpha'), types.CL_String('Beta'),  types.CL_String('Delta'),
    #                                types.CL_String('Gamma'),  types.CL_String('Epsilon')])})

    # session: ModuleBytes = ModuleBytes(
    #     module_bytes=pycspr.read_wasm(ctx.wasm_path),
    #     args={
    #         "amount": types.CL_U512(2500000000),
    #         "target": types.CL_PublicKey.from_public_key(ctx.receiver_key),
    #         # "target": types.CL_ByteArray(ctx.receiver_key.account_hash),
    #         # "id": pycspr.types.CL_Option(pycspr.types.CL_U64(200), pycspr.types.CL_U64).value,
    #         "String": types.CL_String('ACME'),
    #         # "u8": types.CL_U8(8),
    #         # "u32": types.CL_U32(100000),
    #         # "u64": types.CL_U32(1000000),
    #         # "u256": types.CL_U256(100000000000),
    #         # "i32": types.CL_I32(99999),
    #         # "i64": types.CL_I32(9999999),
    #         # "bool": types.CL_Bool(True),
    #         # "bytearray": types.CL_ByteArray(b'01ec7ff7b401fd62efa877b0a88295928fc1ecd93fd3cc6d58373dd38f098724be'),
    #         # "key": types.CL_Key(b'016ff3127d815871618b6f639cf4a4a2df4edeacb8a0df662822707a5e570c9d32', types.CL_KeyType.HASH),
    #         # # "publickey": types.CL_PublicKey(pycspr.KeyAlgorithm.ED25519, b'01ee5c4b8fed1d3b9ad0c4e491d3d5fe2b4a9d9cf04c6fc429c2da4e619a449919'),
    #         # "option": types.CL_Option(types.CL_Bool(True), types.CL_Bool).value,
    #         # "tuple1": types.CL_Tuple1(types.CL_String('ACME')),
    #         # "tuple2": types.CL_Tuple2(types.CL_String('ACME'), types.CL_U32(10000)),
    #         # "tuple3": types.CL_Tuple3(types.CL_String('ACME'), types.CL_U32(10000), types.CL_Bool(False)),
    #         # "list": types.CL_List([types.CL_String('Alpha'), types.CL_String('Beta'),  types.CL_String('Delta'),
    #         #                        types.CL_String('Gamma'),  types.CL_String('Epsilon')])
    #     }
    # )