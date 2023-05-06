import asyncio

from pycspr import NodeEventChannel, NodeEventType
from totaltimeout import Timeout


def call_async_function(ctx, function):
    return asyncio.run(function(ctx))


async def step_event(ctx):
    await ctx.sdk_client.await_n_events(NodeEventChannel.main, NodeEventType.Step, 1)


async def block_event(ctx) -> dict:
    transfer_block_sdk = {}
    for t in Timeout(120):
        transfer_block_sdk = await ctx.sdk_client.await_n_events(NodeEventChannel.main, NodeEventType.BlockAdded, 1)
        print(transfer_block_sdk)
        if len(transfer_block_sdk['BlockAdded']['block']['body']['transfer_hashes']) > 0:
            break

    return transfer_block_sdk
