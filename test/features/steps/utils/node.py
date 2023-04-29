import os

import pycspr


# _PATH_TO_NCTL_ASSETS = pathlib.Path(os.getenv("NCTL")) / "assets" / "net-1"
def CLIENT() -> pycspr.NodeClient:
    return pycspr.NodeClient(pycspr.NodeConnection(
        host="localhost",
        port_rest=14101,
        port_rpc=11101,
        port_sse=18101
    ))

def NODE_HOST() -> str:
    return os.getenv("PYCSPR_TEST_NODE_HOST", "localhost")
def NODE_PORT_REST() -> str:
    return os.getenv("PYCSPR_TEST_NODE_PORT_REST", 14101)
def NODE_PORT_RPC() -> str:
    return os.getenv("PYCSPR_TEST_NODE_PORT_RPC", 11101)

def NODE_PORT_SSE() -> str:
    return os.getenv("PYCSPR_TEST_NODE_PORT_SSE", 18101)
