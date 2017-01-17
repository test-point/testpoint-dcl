Feature: URN encoded Identifiers
    As an eInvoicing participant,
    I need to URN encode business identifiers
    So that I can form a valid DCL query

Scenario Outline: urn encoded ABN 33767197359 (LOWER CASE urn)
    Given I know a business has the identifier 33767197359
    And I know the identifier type is ABN
    When I calculate NID format identifier
    Then I get the URN urn:oasis:names:tc:ecore:partyid-type:iso6523:0151::33767197359

Scenario Outline: urn encoded ABN 33767197359 (MIXED CASE urn)
    Given I know a business has the identifier 33767197359
    And I know the identifier type is ABN
    When I calculate NID format identifier
    Then I get the URN uRn:oasis:Names:TC:ecore:partyid-TYPE:iSo6523:0151::33767197359

Scenario Outline: urn encoded ABN 33767197359 (UPPER CASE urn)
    Given I know a business has the identifier 33767197359
    And I know the identifier type is ABN
    When I calculate NID format identifier
    Then I get the URN URN:OASIS:NAMES:TC:ECORE:PARTYID-TYPE:ISO6523:0151::33767197359

Scenario Outline: urn encoded ABN 14247983785
    Given I know a business has the identifier 14247983785
    And I know the identifier type is ABN
    When I calculate NID format identifier
    Then I get the URN urn:oasis:names:tc:ecore:partyid-type:iso6523:0151::14247983785

Scenario Outline: urn encoded ABN 67008125522
    Given I know a business has the identifier 67008125522
    And I know the identifier type is ABN
    When I calculate NID format identifier
    Then I get the URN urn:oasis:names:tc:ecore:partyid-type:iso6523:0151::67008125522

Scenario Outline: urn encoded ABN 76031101072
    Given I know a business has the identifier 76031101072
    And I know the identifier type is ABN
    When I calculate NID format identifier
    Then I get the URN urn:oasis:names:tc:ecore:partyid-type:iso6523:0151::76031101072

Scenario Outline: urn encoded ABN 17102364628
    Given I know a business has the identifier 17102364628
    And I know the identifier type is ABN
    When I calculate NID format identifier
    Then I get the URN urn:oasis:names:tc:ecore:partyid-type:iso6523:0151::17102364628
