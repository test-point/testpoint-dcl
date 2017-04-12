Feature: Accredited Service Provider can update his public (but not all) information in the DCL.
    As an Accredited Service Provider
    I need to update my public (but not all) information in the DCL.
    So that I keep my record updated for Accredited Service Provider.
# Section 3.4.1 @ "DCL-BusinessRequirements" Document
# ID: 38
# User Interface

Scenario outline: editing ASP information
Given I am authorized in ASP portal Accredited Service Provider
When I am at "Update information" page
Then I am able to change <Field>
When I change <Field> value
And click "Save" button
Then I am able to see changed value

Examples:
|Field|
|Client Certificates|
|Server Certificates|
|Physical Address|
|Website|
|Contact Email|
|Contact Name|
|Position Title|
|Contact Email|
|Phone Number|

Given I am authorized in ASP portal Accredited Service Provider
When I am at "Update information" page
Then I am not able to change "Service provider ID" field value

####### Conditions to be covered on Scenarios #######
# Form should have all public fields of the addition form
      # Certificates:
          # o Client Certificates
          # o Server Certificates
      # Addresses:
          # o Physical Address;
          # o Website
          # o Contact Email
      # Nominated Contact Points:
          # • Contact Name
          # • Position Title
          # • Contact Email
          # • Phone Number
#???# User authenticated using
# Only authorized user can access this page
