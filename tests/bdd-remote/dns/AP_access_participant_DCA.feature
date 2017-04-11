Feature: Access Point access the Digital Capability Address of a participant
    As an Access Point
    I need to access the Digital Capability Address of a participant
    So that
# Section 3.1.1 @ "DCL-BusinessRequirements" Document
# ID: 26
# Section 8.1, 7.2 & 7.3 @ "DCL Implementation Guide" Document
# Usecases @ Appendix A @ "DCL Implementation Guide" Document
    # SUC006 Lookup Digital Capability Publisher Alias Address
# DNS

Given I am Access Point
When I create correct DNS domain name for participant
And I send NAPTR request about that name
Then in response I get correctly formatted U-NAPTR resource record
And that record contains Digital Capability Address of participant

Given I am Access Point
When I create incorrect DNS domain name for participant
And I send NAPTR request about that name
Then in response I get "Refused" response code

Given I am Access Point
When I create correct DNS domain name for nonexistent participant
And I send NAPTR request about that name
Then in response I get "NXDomain" response code

### Conditions to be covered on Scenarios

# The request must be structured as
    # B-<Hash over participant id>.<digital-capability-locator-domain-name>
# DNS name structure
    # b-<Hash over participantID>.[scheme].<DCL-Domain>
    # Note:[scheme] has not been used in the initial implementation of the DCL.
# The response must be a correctly formatted U-NAPTR resource record
# The URI component of the U-NAPTR record will conform with the Council’s profile of the BDX-Location specification.
# "Refused" response code should be provided when the DNS DCL-Domain value is incorrect.
# "NXDomain" response code should be provided when the ParticipantID cannot be found.
# When Address of a recipient’s capability has been cached and the Time-To-Life has not expired). The cached version wikk be served and the DCL does not need to be queried
