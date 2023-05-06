import asyncio

from pycspr import NodeEventChannel, NodeEventType
from totaltimeout import Timeout


# Various async functions

def call_async_function(ctx, function):
    return asyncio.run(function(ctx))


async def step_event(ctx):
    await ctx.sdk_client.await_n_events(NodeEventChannel.main, NodeEventType.Step, 1)


async def block_event(ctx) -> dict:

    transfer_block_sdk = {}
    timeout = Timeout(120)

    for t in timeout:
        transfer_block_sdk = await ctx.sdk_client.await_n_events(NodeEventChannel.main, NodeEventType.BlockAdded, 1)
        print('Seconds remaining: ' + str(int(timeout.time_left())), transfer_block_sdk)
        if len(transfer_block_sdk['BlockAdded']['block']['body']['transfer_hashes']) > 0:
            break

    if len(transfer_block_sdk['BlockAdded']['block']['body']['transfer_hashes']) == 0:
        raise TimeoutError("Failed to find the required block")

    return transfer_block_sdk
