Feature: HexDigest of URN encoded business identifier
    As an eInvoicing participant,
    I need to calculate the MD5 hexdigest of a urn encoded business identifier
    So that I can form a valid DCL query

Scenario Outline: hexdigest of urn encoded ABN 14247983785 (LOWER CASE hexdigest)
    Given I know a business has the identifier 14247983785
    And I know the identifier type is ABN
    When I calculate the MD5 hexdigest of the NID format identifier
    Then I get the value bd9aaa006d6a9ee5856da34d3b64cfa7

Scenario Outline: hexdigest of urn encoded ABN 14247983785 (MIXED CASE hexdigest)
    Given I know a business has the identifier 14247983785
    And I know the identifier type is ABN
    When I calculate the MD5 hexdigest of the NID format identifier
    Then I get the value bD9aAa006D6A9ee5856DA34d3b64cfA7

Scenario Outline: hexdigest of urn encoded ABN 14247983785 (UPPER CASE hexdigest)
    Given I know a business has the identifier 14247983785
    And I know the identifier type is ABN
    When I calculate the MD5 hexdigest of the NID format identifier
    Then I get the value BD9AAA006D6A9EE5856DA34D3B64CfA7

Scenario Outline: hexdigest of urn encoded ABN 17102364628
    Given I know a business has the identifier 17102364628
    And I know the identifier type is ABN
    When I calculate the MD5 hexdigest of the NID format identifier
    Then I get the value 4d309c55f016252f520da17b32b83dd7

Scenario Outline: hexdigest of urn encoded ABN 33767197359
    Given I know a business has the identifier 33767197359
    And I know the identifier type is ABN
    When I calculate the MD5 hexdigest of the NID format identifier
    Then I get the value 94dee132ff9f681ecb17a8d0efc43270

Scenario Outline: hexdigest of urn encoded ABN 67008125522
    Given I know a business has the identifier 67008125522
    And I know the identifier type is ABN
    When I calculate the MD5 hexdigest of the NID format identifier
    Then I get the value f93c9ef583d55e05a9a0bab003386760

Scenario Outline: hexdigest of urn encoded ABN 76031101072
    Given I know a business has the identifier 76031101072
    And I know the identifier type is ABN
    When I calculate the MD5 hexdigest of the NID format identifier
    Then I get the value 2c999502c2abc96bdd6ae7cb1813064c
