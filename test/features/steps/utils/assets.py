# NCTL asset functions
import pycspr
from pycspr import KeyAlgorithm


def get_user_asset_path(path, network, user, file):
    return path + "/net-" + network + "/" + user + "/" + file


def get_user_asset(path, network, user, file):
    return open(path + "/net-" + network + "/" + "user-" + user + "/" + file).read()


def get_user_hex_public_key(ctx, network, usr):

    ctx.sender_key = pycspr.parse_private_key(
        ctx.get_user_asset_path(ctx.ASSETS_ROOT, network, usr, "secret_key.pem"),
        KeyAlgorithm.ED25519.name,
    )


def get_faucet_hex_public_key(ctx):
    ctx.sender_key = pycspr.parse_private_key(
        ctx.ASSETS_ROOT + '/net-1/faucet/secret_key.pem',
        KeyAlgorithm.ED25519.name,
    )


