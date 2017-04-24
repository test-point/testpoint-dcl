Feature: Digital Capability Publisher update a participant record to point to his DCP
    As a Digital Capability Publisher
    I need to update a participant record to point to my DCP
    So that a business can seamlessly transition between service providers

# > Subject to agreement on Business Process by the DCL Working Group.

# Section 3.2.1 @ "DCL-BusinessRequirements" Document
# ID: 20
# REST/JSON or REST/XML API

Given I am accredited DCP with valid Client Sertificate
When I send PUT request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants/{participantId}
And body of request has correct JSON format with "validTill" field to update
Then in response I should get code code "200" with correct JSON response
And response should contain updated data

Given I am accredited DCP with valid Client Sertificate
When I send PUT request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants/{participantId}
And body of request has correct XML format with "validTill" field to update
Then in response I should get code code "200" with correct XML response
And response should contain updated data

Given I know of accredited DCP1 with valid Client Certificate
And I know of accredited DCP2 with valid Client Certificate
And I have date of transition between DCPs
And DCP2 prenotified DCP1 about transition between DCPs and submited the confirmation to the DCL
When DCP1 send PUT request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants/{participantId}
And body of request has correct JSON format with "validTill" field equal to transition date
Then participant_id record is updated
When DCP2 sends PUT request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants/{participantId}
And body of request has correct JSON format with "validFrom" field equal to transition date
Then participant_id record sucessfully migrated from DCP1 to DCP2
And no down time occured

Given participant with participantId hac existing relationship with DCP1 with valid Client Certificate
And I know of accredited DCP2 with valid Client Certificate
And DCL has no confirmation about transition of participant between DCPs
When DCP2 sends PUT request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants/{participantId}
And body of request has correct JSON format with "validFrom" field
Then in response DCP2 should get code "409" with "DCL-0002" in response
And no transition occured

Given I am accredited DCP with invalid Client Certificate
When I send PUT request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants/{participantId}
And body of request has correct JSON format
Then in response I should get code "403" with error in response

Given I am accredited DCP with valid Client Certificate
When I send PUT request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants/{participantId}
And body of request has wrong JSON format
Then in response I should get code "400" with error in response

Given I am accredited DCP with valid Client Certificate
When I send PUT request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants/{participantId}
And body of request has correct JSON format with wrong capabilityPublisherID
Then in response I should get code "403" with error in response

Given I am nonaccredited DCP with valid Client Certificate
When I send PUT request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants/{participantId}
And body of request has correct JSON format
Then in response I should get code "422" with "DCL-0001" error in response

Given I am accredited DCP with valid Client Certificate
When I send PUT request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants/{participantId}
And body of request has correct JSON format with incorrect participantId
Then in response I should get code "404" with error in response

Given I am accredited DCP with valid Client Certificate
And I know DCL with invalid Server certificate
When I try to establish https connection with that DCL
Then I tear down connection

### Conditions to be covered on Scenarios

# A gaining DCP must pre notify the losing DCP of the transition and submit the confirmation/acknowledgement with the update request to the DCL
# The existing relationship is not deleted, but rather end-dated.
# The update request can submit a future date time for the update to take effect so long as it is less that 30 days from the original notification to the existing DCP.
# TLS 1.2 Mutual (Client and Server) Certificate Authentication
