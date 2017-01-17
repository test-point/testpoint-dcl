Feature: Calculate DCL query string
    As an eInvoicing participant,
    I need to calculate a valid DCL query string
    So I can access the DCL query API through DNS


Scenario Outline: Calculate DCL query for ABN 33767197359 at dcl.testpoint.io
    Given I know a business has the identifier 33767197359
    And I know the identifier type is ABN
    And the DCL domain name is dcl.testpoint.io
    When I calculate the DNS query string
    Then I get the address b-94dee132ff9f681ecb17a8d0efc43270.dcl.testpoint.io

Scenario Outline: Calculate DCL query for ABN 33767197359 at dcl.testpoint.io (CASE INSENSITIVE DNS)
    Given I know a business has the identifier 33767197359
    And I know the identifier type is ABN
    And the DCL domain name is DCL.TestPoint.io
    When I calculate the DNS query string
    Then I get the address b-94dee132ff9f681ecb17a8d0efc43270.dcl.testpoint.io

Scenario Outline: Calculate DCL query for ABN 33767197359 at dcl.testpoint.io (CASE INSENSITIVE HEXDIGEST)
    Given I know a business has the identifier 33767197359
    And I know the identifier type is ABN
    And the DCL domain name is dcl.testpoint.io
    When I calculate the DNS query string
    Then I get the address b-94DEE132FF9F681ECB17A8D0EFC43270.dcl.testpoint.io

Scenario Outline: Calculate DCL query for ABN 33767197359 at dcl.testpoint.io (CASE INSENSITIVE QUERY)
    Given I know a business has the identifier 33767197359
    And I know the identifier type is ABN
    And the DCL domain name is dcl.testpoint.io
    When I calculate the DNS query string
    Then I get the address B-94DEE132FF9F681ECB17A8D0EFC43270.DCL.TESTPOINT.IO

Scenario Outline: Calculate DCL query for ABN 14247983785 at foo.org
    Given I know a business has the identifier 14247983785
    And I know the identifier type is ABN
    And the DCL domain name is foo.org
    When I calculate the DNS query string
    Then I get the address b-bd9aaa006d6a9ee5856da34d3b64cfa7.foo.org

Scenario Outline: Calculate DCL query for ABN 67008125522 at bar.gov.au
    Given I know a business has the identifier 67008125522
    And I know the identifier type is ABN
    And the DCL domain name is bar.gov.au
    When I calculate the DNS query string
    Then I get the address b-f93c9ef583d55e05a9a0bab003386760.bar.gov.au

Scenario Outline: Calculate DCL query for ABN 76031101072 at dcl.business.gov.au
    Given I know a business has the identifier 76031101072
    And I know the identifier type is ABN
    And the DCL domain name is dcl.business.gov.au
    When I calculate the DNS query string
    Then I get the address b-2c999502c2abc96bdd6ae7cb1813064c.dcl.business.gov.au

Scenario Outline: Calculate DCL query for ABN 17102364628 at dcl.business.gov.au
    Given I know a business has the identifier 17102364628
    And I know the identifier type is ABN
    And the DCL domain name is dcl.business.gov.au
    When I calculate the DNS query string
    Then I get the address b-4d309c55f016252f520da17b32b83dd7.dcl.business.gov.au
