from behave import *

use_step_matcher("re")

# Step definitions for info_get_validator_changes cucumber tests


@given("that the info_get_validator_changes method is invoked against a node")
def info_get_validator_changes_is_invoked(ctx):
    print('that the info_get_validator_changes method is invoked against a node')

    ctx.validators_changes = ctx.sdk_client.get_validator_changes()

    ctx.expected_validator_changes = ctx.nctl_requests.get_info_get_validator_changes()
    assert ctx.expected_validator_changes


@then("a valid info_get_validator_changes_result is returned")
def a_valid_result_is_returned(ctx):
    print('a valid info_get_validator_changes_result is returned')

    assert ctx.validators_changes == ctx.expected_validator_changes['result']['changes']


@step("the info_get_validator_changes_result contains a valid API version")
def a_valid_api_is_returned(ctx):
    print('the info_get_validator_changes_result contains a valid API version')

    # TODO info_get_validator_changes doesn't return the api version
