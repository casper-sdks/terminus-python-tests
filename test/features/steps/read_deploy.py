import json
import os
import pathlib
import typing

from behave import *

use_step_matcher("re")


# Step definitions for read deploy cucumber tests

_PATH_TO_JSON = pathlib.Path(os.path.dirname(__file__)) / "json"


def _read_deploy_json(fname: str, parser: typing.Callable = json.load):
    with open(_PATH_TO_JSON / fname) as fstream:
        return fstream.read() if parser is None else parser(fstream)


@given('that the "(.*)" JSON deploy is loaded')
def the_transfer_json_is_loaded(ctx, deploy_json):
    print('that the "{}" JSON deploy is loaded'.format(deploy_json))

    # ctx.sdk_client.send_deploy(_read_deploy_json(deploy_json))

    raise NotImplementedError(u'read_deploy not implemented')


@then("a valid transfer deploy is created")
def a_valid_transfer_deploy_is_created(ctx):
    print('a valid transfer deploy is created')


@step('the deploy hash is "(.*)"')
def the_deploy_hash_is(ctx, deploy_hash):
    print('the deploy hash is {}'.format(deploy_hash))


@step('the account is "(.*)"')
def the_account_is(ctx, account):
    print('the account is {}'.format(account))


@step('the timestamp is "(.*)"')
def the_timestamp_is(ctx, timestamp):
    print('the timestamp is {}'.format(timestamp))


@step("the ttl is (.*)m")
def the_ttl_is(ctx, ttl):
    print('the ttl is {}'.format(ttl))


@step("the gas price is (.*)")
def step_impl(ctx, gas_price):
    print('the gas price is {}'.format(gas_price))


@step('the body_hash is "(.*)"')
def the_body_hash_is(ctx, body_hash):
    print('the body hash is {}'.format(body_hash))


@step('the chain name is "(.*)"')
def the_chain_name_is(ctx, chain_name):
    print('the chain name is {}'.format(chain_name))


@step('dependency (.*) is "(.*)"')
def dependency_is(ctx, dependency, value):
    print('dependency {} is {}'.format(dependency, value))


@step("the payment amount is (.*)")
def payment_amount_is(ctx, payment_amount):
    print('the payment amount is {}'.format(payment_amount))


@step("the session is a transfer")
def session_is_transfer(ctx):
    print('the session is a transfer')


@step('the session "(.*)" is (.*)')
def the_session_amount_is(ctx, key, value):
    print('the session {} is {}'.format(key, value))


@step('the session "(.*)" type is "(.*)"')
def the_session_type_is(ctx, key, value):
    print('the session {} type is {}'.format(key, value))


@step('the session "(.*)" bytes is "(.*)"')
def the_session_bytes_is(ctx, key, value):
    print('the session {} bytes is {}'.format(key, value))


@step('the session "(.*)" parsed is "(.*)"')
def the_session_amount_parsed_is(ctx, key, value):
    print('the session {} parsed is {}'.format(key, value))


@step("the deploy has (.*) approval")
def the_deploy_has_approval(ctx, approval):
    print('the deploy has {} approval'.format(approval))


@step('the approval signer is "(.*)"')
def the_approval_signer_is(ctx, signer):
    print('the approval signer is {}'.format(signer))


@step('the approval signature is "(.*)"')
def the_signature_is(ctx, signature):
    print('the approval signature is {}'.format(signature))

