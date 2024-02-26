import pycspr


# Creates a Python SDK client

def client(config) -> pycspr.NodeClient:
    return pycspr.NodeClient(pycspr.NodeConnection(
        host=config.get_node_host(),
        port_rest=config.get_node_port_rest(),
        port_rpc=config.get_node_port_rpc(),
        port_sse=config.get_node_port_sse(),
    ))


def client_spec(config) -> pycspr.NodeClient:
    return pycspr.NodeClient(pycspr.NodeConnection(
        host=config.get_node_host(),
        port_rest=config.get_node_port_rest(),
        port_rpc=config.get_node_port_rpc(),
        port_sse=config.get_node_port_sse(),
        port_rpc_speculative=config.get_node_port_spec()
    ))
