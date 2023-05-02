from steps.utils.exec import NCTLExec
from steps.utils.node import CLIENT

# Steps to run at specific times in the scenarios


def before_all(context):
    context.sdk_client = CLIENT()
    context.nctl_client = NCTLExec()


def before_scenario(scenario, context):
    print('Before scenario executed')


def after_feature(scenario, context):
    print('After feature executed')


def after_all(context):
    print('After all executed')
