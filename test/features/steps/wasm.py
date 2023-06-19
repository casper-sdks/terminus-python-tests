import io
import os
import pathlib

from behave import *
from pycspr.types import *

from test.features.steps.utils.assets import *

use_step_matcher("re")


@given('that a smart contract "(.*)" is located in the "(.*)" folder')
def that_a_smart_contract_exists(ctx, file, location):
    print('that a smart contract "{}" is located in the "{}" folder'.format(file, location))

    ctx.wasm_path = pathlib.Path(os.path.dirname(__file__)) / location / file
    ctx.wasm_stream = io.open(ctx.wasm_path, 'rb')

    assert ctx.wasm_stream


@then("when the wasm is loaded as from the file system")
def the_contract_is_loaded(ctx):
    print('when the wasm is loaded as from the file system')

    _bytes = ctx.wasm_stream.read()
    assert len(_bytes) == 189336

    get_faucet_hex_public_key(ctx)

    params: DeployParameters = \
        pycspr.create_deploy_parameters(
            account=ctx.sender_key,
            chain_name='casper-net-1'
            )

    payment: ModuleBytes = \
        pycspr.create_standard_payment(50000000000)

    session: ModuleBytes = ModuleBytes(
        module_bytes=pycspr.read_wasm(ctx.wasm_path),
        args={
            "token_decimals": CL_U8(11),
            "token_name": CL_String('Acme Token'),
            "token_symbol": CL_String('ACME'),
            "token_total_supply": CL_U256(1000000000000000),
        }
    )

    deploy: Deploy = pycspr.create_deploy(params, payment, session)

    deploy.approve(ctx.sender_key)
    ctx.deploy_hash = ctx.sdk_client.send_deploy(deploy)

    assert ctx.deploy_hash
    print(ctx.deploy_hash)


