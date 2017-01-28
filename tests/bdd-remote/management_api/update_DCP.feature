Feature: Simplified DCP update
    As an eInvoicing participant,
    I need to update my DCP entry with the simplified DCL web interface
    So that I can chose my DCP provider

#
# simplified DCP update interface is not compliant with the
# ADBC specification v1.0-draft
#
# Main difference is that it leverages an OIDC IDP, such as
# https://idp.testpoint.io (rather than client certificates).
#

Scenario: Log in and see the update form
    Given I have ABN credentials at the DCL web interface
    When I authenticate
    When I go "/ui/"
    Then I see "Update DCP"
    Then I click "Update DCP"
    Then I see "Here you can change your DCP to any domain name."
    And I see "New DCP Value"


Scenario: Update DCP value
    Given I have ABN credentials at the DCL web interface
    When I authenticate
    When I go "/ui/"
    Then I see "Update DCP"
    Then I click "Update DCP"
    Then I see "Here you can change your DCP to any domain name."
    And I see "New DCP Value"
    Then I fill the 'new_smp_value' field by 'just.another.dcp.testpoint.io' value
    Then I submit the form
    And I see "Value update scheduled"

# Scenario: Check the update form
#     Given I have ABN credentials at the DCL web interface
#     When I authenticate
#     And click the "update my DCP" button
#     Then I see the DCP update form

# Scenario: Check the save button
#     Given I have ABN credentials at the DCL web interface
#     When I authenticate
#     And click the "update my DCP" button
#     And I enter new value in the DCP update form
#     Then I see "save" button

# Scenario: Check the confirm button
#     Given I have ABN credentials at the DCL web interface
#     When I authenticate
#     And click the "update my DCP" button
#     And I enter new value in the DCP update form
#     And then I click the "save" button
#     Then I see the "confirm" button

# Scenario: Save changes to the DCP
#     Given I have ABN credentials at the DCL web interface
#     When I authenticate
#     And click the "update my DCP" button
#     And I enter new value in the DCP update form
#     And then I click the "save" button
#     And I click the "confirm" button
#     Then I see "DCP updated" message

