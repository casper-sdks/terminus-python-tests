import pycspr


# Creates a Python SDK client

def client_rpc(config) -> pycspr.NodeRpcClient:
    return pycspr.NodeRpcClient(pycspr.NodeConnectionInfo(
        host=config.get_node_host(),
        port_rest=config.get_node_port_rest(),
        port_rpc=config.get_node_port_rpc(),
        port_sse=config.get_node_port_sse(),
    ))


def client_sse(config) -> pycspr.NodeSseClient:
    return pycspr.NodeSseClient(pycspr.NodeConnectionInfo(
        host=config.get_node_host(),
        port_rest=config.get_node_port_rest(),
        port_rpc=config.get_node_port_rpc(),
        port_sse=config.get_node_port_sse(),
    ))


def client_spec(config) -> pycspr.NodeSpeculativeRpcClient:
    return pycspr.NodeSpeculativeRpcClient(pycspr.NodeConnectionInfo(
        host=config.get_node_host(),
        port_rest=config.get_node_port_rest(),
        port_rpc=config.get_node_port_rpc(),
        port_sse=config.get_node_port_sse(),
        port_rpc_speculative=config.get_node_port_spec()
    ))
