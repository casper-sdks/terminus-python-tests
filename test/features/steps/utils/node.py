import pycspr.api.rpc


# Creates a Python SDK client

def client_rpc(config) -> pycspr.NodeRpcClient:
    return pycspr.NodeRpcClient(pycspr.NodeRpcConnectionInfo(
        host=config.get_node_host(),
        port=config.get_node_port_rpc()
    ))


def client_sse(config) -> pycspr.NodeSseClient:
    return pycspr.NodeSseClient(pycspr.NodeSseConnectionInfo(
        host=config.get_node_host(),
        port=config.get_node_port_sse()
    ))


def client_spec(config) -> pycspr.NodeSpeculativeRpcClient:
    return pycspr.NodeSpeculativeRpcClient(pycspr.NodeSpeculativeRpcConnectionInfo(
        host=config.get_node_host(),
        port=config.get_node_port_spec()
    ))
