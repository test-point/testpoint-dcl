Feature: Simplified SMP update
    As an eInvoicing participant,
    I need to update my SMP entry with the simplified DCL web interface
    So that I can chose my SMP provider

#
# simplified SMP update interface is not compliant with the
# ADBC specification v1.0-draft
#
# Main difference is that it leverages an OIDC IDP, such as
# https://idp.testpoint.io (rather than client certificates).
#

Scenario: Log in and see the update form
    Given I have ABN credentials at the DCL web interface
    When I authenticate
    Then I see "Update SMP"
    Then I click "Update SMP"
    Then I see "Here you can change your DCP to any domain name."
    And I see "New SMP Value"


Scenario: Update SMP value
    Given I have ABN credentials at the DCL web interface
    When I authenticate
    # When I go "/"
    Then I see "Update SMP"
    Then I click "Update SMP"
    Then I see "Here you can change your DCP to any domain name."
    And I see "New SMP Value"
    Then I fill the 'new_smp_value' field by 'just.another.smp.testpoint.io' value
    Then I submit the form
    And I see "Value update scheduled"

# Scenario: Check the update form
#     Given I have ABN credentials at the DCL web interface
#     When I authenticate
#     And click the "update my SMP" button
#     Then I see the SMP update form

# Scenario: Check the save button
#     Given I have ABN credentials at the DCL web interface
#     When I authenticate
#     And click the "update my SMP" button
#     And I enter new value in the SMP update form
#     Then I see "save" button

# Scenario: Check the confirm button
#     Given I have ABN credentials at the DCL web interface
#     When I authenticate
#     And click the "update my SMP" button
#     And I enter new value in the SMP update form
#     And then I click the "save" button
#     Then I see the "confirm" button

# Scenario: Save changes to the SMP
#     Given I have ABN credentials at the DCL web interface
#     When I authenticate
#     And click the "update my SMP" button
#     And I enter new value in the SMP update form
#     And then I click the "save" button
#     And I click the "confirm" button
#     Then I see "SMP updated" message

