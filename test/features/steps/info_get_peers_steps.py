from behave import *

use_step_matcher("re")

# Step definitions for info_get_peers cucumber tests


@given("that the info_get_peers RPC method is invoked against a node")
def info_get_peers_invoked(ctx):
    print('that the info_get_peers RPC method is invoked against a node')
    ctx.peer_data = ctx.sdk_client_rpc.get_node_peers()


@then("the node returns an info_get_peers_result")
def peers_result_is_returned(ctx):
    print('the node returns an info_get_peers_result')
    assert ctx.peer_data


@step('the info_get_peers_result has an API version of "(.*)"')
def peers_result_has_api_version(ctx, api_version):
    print('the info_get_peers_result has an API version of {}'.format(api_version))

    # TODO api version not returned in the response


@step('the info_get_peers_result contains (.*) peers')
def the_result_contains_n_peers(ctx, peers):
    print('he info_get_peers_result contains {} peers'.format(peers))

    assert len(ctx.peer_data) == int(peers)


@step('the info_get_peers_result contains a valid peer with a port number of (.*)')
def step_impl(ctx, port):
    print('the info_get_peers_result contains a valid peer with a port number of {}'.format(port))

    assert next((peers for peers in ctx.peer_data if port in peers['address']), None)

