Feature: Nested Options

  Scenario: Nested Options
    Given that a nested Option has an inner type of Option with a type of String and a value of "77541f74-c0b6-428e-9f53-ddd298f1bc8c"
    Then the inner type is Option with a type of String and a value of "77541f74-c0b6-428e-9f53-ddd298f1bc8c"
    And the bytes are "01000000"
    Given that the nested Option is deployed in a transfer
    And the transfer containing the nested Option is successfully executed
    When the Option is read from the deploy
    Then the inner type is Option with a type of String and a value of "77541f74-c0b6-428e-9f53-ddd298f1bc8c"
    And the bytes are "01000000"
