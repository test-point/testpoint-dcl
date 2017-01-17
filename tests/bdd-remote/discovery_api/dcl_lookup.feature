Feature: DCL lookup
    As an eInvoicing participant,
    I need to make DCL queries
    so that I can locate the SMP for identified businesses

#
# examples are loaded from fixtures.py rather than coded here
# to allow for alternate data fixtures at alternate test targets
#
# the only assumption is there are exactly 5 examples
#

Scenario: Check reference values example 1
    Given I know a DCL with expected lookup values 
    When I query the DCL for the first lookup fixture
    Then the results match the first lookup fixture expected value

Scenario: Check reference values example 2
    Given I know a DCL with expected lookup values 
    When I query the DCL for the second lookup fixture
    Then the results match the second lookup fixture expected value

Scenario: Check reference values example 3
    Given I know a DCL with expected lookup values 
    When I query the DCL for the third lookup fixture
    Then the results match the third lookup fixture expected value

Scenario: Check reference values example 4
    Given I know a DCL with expected lookup values 
    When I query the DCL for the fourth lookup fixture
    Then the results match the fourth lookup fixture expected value

Scenario: Check reference values example 5
    Given I know a DCL with expected lookup values 
    When I query the DCL for the fifth lookup fixture
    Then the results match the fifth lookup fixture expected value
