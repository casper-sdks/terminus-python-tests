import os

from steps.utils.config import CONFIG
from steps.utils.exec import NCTLExec
from steps.utils.node import client


# Steps to run at specific times in the scenarios


def before_all(ctx):
    ctx.config = CONFIG()
    ctx.sdk_client = client(ctx.config)
    ctx.nctl_client = NCTLExec(ctx.config)
    ctx.ASSETS_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../assets/'))
