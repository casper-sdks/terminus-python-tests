Feature: Any Values
  Scenario: Simple Any Values
    Given an Any value contains a "Bool" value of "true"
    Then the any value's bytes are "01"
    Given that the any value is deployed in a transfer as a named argument
    And the transfer containing the any value is successfully executed
    When the any is read from the deploy
    Then the any value's bytes are "01"
    And the type of the any is "Bool" with a value of "true"

    Given an Any value contains a "ByteArray" value of "d2029649"
    Then the any value's bytes are "d2029649"
    Given that the any value is deployed in a transfer as a named argument
    And the transfer containing the any value is successfully executed
    When the any is read from the deploy
    Then the any value's bytes are "d2029649"

    Given an Any value contains a "I32" value of "1234567890"
    Then the any value's bytes are "d2029649"
    Given that the any value is deployed in a transfer as a named argument
    And the transfer containing the any value is successfully executed
    When the any is read from the deploy
    Then the any value's bytes are "d2029649"

    Given an Any value contains a "I64" value of "102030405060708090"
    Then the any value's bytes are "fac6eee11c7c6a01"
    Given that the any value is deployed in a transfer as a named argument
    And the transfer containing the any value is successfully executed
    When the any is read from the deploy
    Then the any value's bytes are "fac6eee11c7c6a01"

    Given an Any value contains a "String" value of "The quick brown fox jumps over the lazy dog."
    Then the any value's bytes are "2c00000054686520717569636b2062726f776e20666f78206a756d7073206f76657220746865206c617a7920646f672e"
    Given that the any value is deployed in a transfer as a named argument
    And the transfer containing the any value is successfully executed
    When the any is read from the deploy
    Then the any value's bytes are "2c00000054686520717569636b2062726f776e20666f78206a756d7073206f76657220746865206c617a7920646f672e"

    Given an Any value contains a "U8" value of "15"
    Then the any value's bytes are "0f"

    Given an Any value contains a "U32" value of "1234567890"
    Then the any value's bytes are "d2029649"
    Given that the any value is deployed in a transfer as a named argument
    And the transfer containing the any value is successfully executed
    When the any is read from the deploy
    Then the any value's bytes are "d2029649"

    Given an Any value contains a "U64" value of "102030405060708090"
    Then the any value's bytes are "fac6eee11c7c6a01"
    Given that the any value is deployed in a transfer as a named argument
    And the transfer containing the any value is successfully executed
    When the any is read from the deploy
    Then the any value's bytes are "fac6eee11c7c6a01"

    Given an Any value contains a "U128" value of "102030405060708090"
    Then the any value's bytes are "08fac6eee11c7c6a01"
    Given that the any value is deployed in a transfer as a named argument
    And the transfer containing the any value is successfully executed
    When the any is read from the deploy
    Then the any value's bytes are "08fac6eee11c7c6a01"

    Given an Any value contains a "U256" value of "102030405060708090102030405060708090"
    Then the any value's bytes are "0ffac696b1fd5d40dc69265dc37ca613"
    Given that the any value is deployed in a transfer as a named argument
    And the transfer containing the any value is successfully executed
    When the any is read from the deploy
    Then the any value's bytes are "0ffac696b1fd5d40dc69265dc37ca613"

    Given an Any value contains a "U512" value of "102030405060708090102030405060708090102030405060708090"
    Then the any value's bytes are "17fac696b19d1300622227dcf324306f3cdea13d09b41001"
    Given that the any value is deployed in a transfer as a named argument
    And the transfer containing the any value is successfully executed
    When the any is read from the deploy
    Then the any value's bytes are "17fac696b19d1300622227dcf324306f3cdea13d09b41001"

    Given an Any value contains a "Any" value of "102030405060708090102030405060708090102030405060708090"
    Then the any value's bytes are "102030405060708090102030405060708090102030405060708090"
    Given that the any value is deployed in a transfer as a named argument
    And the transfer containing the any value is successfully executed
    When the any is read from the deploy
    Then the any value's bytes are "102030405060708090102030405060708090102030405060708090"
