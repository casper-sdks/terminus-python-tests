from behave import *
from pycspr.types import *

from test.features.steps.utils.assets import get_faucet_private_key

use_step_matcher("re")

# Step definitions for state_get_dictionary_item cucumber tests


@given("that the state_get_dictionary_item RCP method is invoked")
def state_get_dictionary_item_invoked(ctx):
    print('that the state_get_dictionary_item RCP method is invoked')

    print('BUG:The get_dictionary_item fails. Code needs implementing in the DictionaryId')

    get_faucet_private_key(ctx)

    dictionary_id = DictionaryID_UniqueKey(
        key='account-hash-' + ctx.sender_key.account_hash.hex()
    )

    ctx.dictionary_item = ctx.sdk_client_rpc.get_dictionary_item(dictionary_id)


@then("a valid state_get_dictionary_item_result is returned")
def valid_state_get_dictionary_item_returned(ctx):
    print('a valid state_get_dictionary_item_result is returned')
