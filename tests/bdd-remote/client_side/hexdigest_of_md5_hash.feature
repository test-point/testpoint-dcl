Feature: Calculate Query String
    As an eInvoicing participant,
    I need to calculate DCL query strings
    so that I can lookup particppant capability

Scenario Outline: Check MD5 calculation correctness
    Given I have string 14247983785
    When I calculate MD5 hexdigest of string
    Then I get hashed value of string 68f746c52284aed8d84db4b20092ead7

Scenario Outline: Check MD5 calculation correctness
    Given I have string 17102364628
    When I calculate MD5 hexdigest of string
    Then I get hashed value of string 17a0a3327bf5a6a0d6663f8881584f44

Scenario Outline: Check MD5 calculation correctness
    Given I have string 33767197359
    When I calculate MD5 hexdigest of string
    Then I get hashed value of string 35b4d4de2e2ce375c14ef34dbd0fe216

Scenario Outline: Check MD5 calculation correctness
    Given I have string 67008125522
    When I calculate MD5 hexdigest of string
    Then I get hashed value of string ed1eda1a59d961f778a41cd4dbed8156

Scenario Outline: Check MD5 calculation correctness
    Given I have string 76031101072
    When I calculate MD5 hexdigest of string
    Then I get hashed value of string b2ecc82e729e5e8ebfc1b16d123e92cb

Scenario Outline: Check MD5 calculation correctness
    Given I have string aaa
    When I calculate MD5 hexdigest of string
    Then I get hashed value of string 47bce5c74f589f4867dbd57e9ca9f808

Scenario Outline: Check MD5 calculation correctness
    Given I have string bbb
    When I calculate MD5 hexdigest of string
    Then I get hashed value of string 08f8e0260c64418510cefb2b06eee5cd

Scenario Outline: Check MD5 calculation correctness
    Given I have string foo
    When I calculate MD5 hexdigest of string
    Then I get hashed value of string acbd18db4cc2f85cedef654fccc4a4d8
