import asyncio

from pycspr import NodeEventChannel, NodeEventType
from pycspr.types import Deploy
from totaltimeout import Timeout


# Various async functions

def call_async_function(ctx, function):
    return asyncio.run(function(ctx))


async def step_event(ctx):
    await ctx.sdk_client_sse.await_n_events(1, NodeEventChannel.main, NodeEventType.Step)


async def block_event(ctx) -> dict:

    transfer_block_sdk = {}
    timeout = Timeout(ctx.timeout)
    block_found = False

    for t in timeout:
        transfer_block_sdk = await ctx.sdk_client_sse.await_n_events(1, NodeEventChannel.main, NodeEventType.BlockAdded)
        print('Seconds remaining: ' + str(int(timeout.time_left())), transfer_block_sdk)
        if ctx.deploy_result.hash.hex() in transfer_block_sdk['BlockAdded']['block']['body']['transfer_hashes']:
            block_found = True
            break

    if not block_found:
        raise TimeoutError("Failed to find the required block")

    return transfer_block_sdk


async def deploy_event(ctx) -> Deploy:

    deploy: Deploy = {}
    timeout = Timeout(ctx.timeout)
    deployed = False

    for t in timeout:
        deploy = ctx.sdk_client_rpc.get_deploy(ctx.deploy.hash)
        # print('Seconds remaining: ' + str(int(timeout.time_left())))
        if len(deploy['execution_results']) > 0:
            deployed = True
            break
    if not deployed:
        raise TimeoutError("Deploy timed out")

    return deploy['execution_results']


