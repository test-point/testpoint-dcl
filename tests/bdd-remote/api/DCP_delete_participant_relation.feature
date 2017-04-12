Feature: Digital Capability Publisher delete existing relationship with a participant
    As a Digital Capability Publisher
    I need to delete(end-date) an existing relationship between a participant and my DCP.
    So that the DCL shows the result of termination of the commercial relationship
# Section 3.2.1 @ "DCL-BusinessRequirements" Document
# ID: 43
# Section 8.3.2 @ "DCL Implementation Guide" Document
# Usecases @ Appendix A @ "DCL Implementation Guide" Document
    # SUC013 Remove Digital Capability Publisher Alias Address
# REST/JSON or REST/XML API

Given I am accredited DCP with valid Client Certificate
When I send DELETE request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants/{participantId}
And body of request has correct JSON format
Then in response I should get code "204"
And relationship for participant with {participantId} should be end-dated

Given I am accredited DCP with valid Client Certificate
When I send DELETE request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants/{participantId}
And body of request has correct XML format
Then in response I should get code "204"
And relationship for participant with {participantId} should be end-dated

Given I am accredited DCP with invalid Client Certificate
When I send DELETE request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants/{participantId}
And body of request has correct JSON format
Then in response I should get code "403" with error in response

Given I am accredited DCP with valid Client Certificate
When I send DELETE request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants/{participantId}
And body of request has wrong JSON format
Then in response I should get code "400" with error in response

Given I am accredited DCP with valid Client Certificate
When I send DELETE request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants/{participantId}
And body of request has correct JSON format with wrong capabilityPublisherID
Then in response I should get code "403" with error in response

#error 422 not described in spec for that method - https://github.com/company-book/capability-lookup/issues/50 (this might not actually be required)
Given I am nonaccredited DCP with valid Client Certificate
When I send DELETE request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants/{participantId}
And body of request has correct JSON format
Then in response I should get code "422" with "DCL-0001" error in response

Given I am accredited DCP with valid Client Certificate
When I send DELETE request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants/{participantId}
And body of request has correct JSON format with incorrect participantIdentifier
Then in response I should get code "400" with error in response

Given I am accredited DCP with valid Client Certificate
When I send DELETE request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants/{participantId}
And body of request has correct JSON format with incorrect participantIdentifierScheme
Then in response I should get code "400" with error in response

Given I am accredited DCP with valid Client Certificate
When I send DELETE request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants/{participantId} with nonexistent participantId
And body of request has correct JSON format with same participantId
Then in response I should get code "404" with error in response

Given I am accredited DCP with valid Client Certificate
And I know participant which have an active relationship with another DCP
When I send DELETE request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants/{participantId}
And body of request has correct JSON format with that participant credentials
Then in response I should get code "409" with "DCL-0002" error in response

Given I am accredited DCP with valid Client Certificate
And I know DCL with invalid Server certificate
When I try to establish https connection with that DCL
Then I tear down connection

### Conditions to be covered on Scenarios

# [DELETE] https://<Digital Capability Locator Domain Name>/api/capabilityPublisher/{capabilityPublisherID}/participants/{participantId}
# TLS 1.2 Mutual (Client and Server) Certificate Authentication
# JSON & XML support
# Error conditions return the corresponding error messages and http status ("204" => "No Content","400" => "bad request","403" => "Forbidden","404" => "Not found","409" => "Conflict", "5xx" => "Server Error")
# HTTP 500 level errors return a sanitised error response that does not expose the internal workings or configuration of the DCL.
# request and response examples available under 8.3.2 @ DCL Implementation Guide

# Success: The Participant’s Digital Address history will be updated to flag the relationship as ‘Cancelled'
# Relationships are not deleted, but rather end-dated.
# If no end date-time is specified then the current date-time (Canberra ACT) is used.
# If the end date-time has occurred/past then the DNS UNAPTR record is marked for deletion ASAP.

# The DCP ID should be a valid ID.
# A DCP can only end-date a participant's relationship for their own DCP.
# A Digital Capability Publisher can only end-date are relationship between a participant and their own service provider record.
# The participant Identifier must meet the structural format requirements of the identifier scheme.
# The participant identifier scheme must be on the Council's list of approved identifiers, as per the Policy on the use of business identifiers.
