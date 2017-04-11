Feature: Access Point know the maximum time to cache (DNS TTL) a participant’s DCP Address
    As an Access Point
    I need to know the maximum time to cache (DNS TTL) a participant’s DCP Address
    So that
# Section 3.1.1 @ "DCL-BusinessRequirements" Document
# ID: 36
# DNS

Given I am Access Point
When I create correct DNS domain name for participant
And I send NAPTR request about that name
Then in response I get correctly formatted U-NAPTR resource record
And that record contains TTL for participant’s DCP Address based on the configured value

Given I am Access Point
And I have results of previous NAPTR request for participant 
And TTL for participant hasn't expired
When I need to send NAPTR request about given participant
Then I can use results of previous request

### Conditions to be covered on Scenarios

# All DNS UNAPTR records are returned with a Time To Live (TTL) based on the configured value
