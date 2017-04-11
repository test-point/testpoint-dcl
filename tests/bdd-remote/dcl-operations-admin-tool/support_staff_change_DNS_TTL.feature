Feature: DCL Operations Support Staff member change default TTL value of DNS
    As a DCL Operations Support Staff member
    I need to change default TTL value of DNS on the DCL Operations Admin Tool
    So that I can control the maximum cache time of a record

# Section 3.1.1 @ "DCL-BusinessRequirements" Document
# @mentioned in story ID: 36
# User Interface

Given I am authorized DCL Operations Support Staff member
When I am at "Configuration" page
Then I should be able to see TTL value of DNS
And default TTL value is 5  minutes

Given I am authorized DCL Operations Support Staff member
When I am at "Configuration" page
Then I should be able to change default TTL value of DNS
And updated value will apply to any new or updated UNAPTR records

### Conditions to be covered on Scenarios

# The default configuration for the TTL will be 5 Minutes;
# The updated value will apply to any new or updated UNAPTR records.
