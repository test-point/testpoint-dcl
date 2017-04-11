Feature: Digital Capability Publisher add a relationship to a participant
    As a Digital Capability Publisher
    I need to add a relationship between a participant and my DCP
    So that
# Section 3.2.1 @ "DCL-BusinessRequirements" Document
# ID: 42
# Section 8.3.1 @ "DCL Implementation Guide" Document
# Usecases @ Appendix A @ "DCL Implementation Guide" Document
    # SUC002 Register Digital Capability Publisher Alias Address
# REST/JSON or REST/XML API

Given I am accredited DCP with valid Client Certificate
When I send POST request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants
And body of request has correct JSON format
Then in response I should get code "201" with hash in response
And hash should be prefixed by "b-"
And hash should be suffixed by hashed participantIdentifier and participantIdentifierScheme combination

Given I am accredited DCP with valid Client Sertificate
When I send POST request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants
And body of request has correct XML format
Then in response I should get code "201" with hash in response
And hash should be prefixed by "b-"
And hash should be suffixed by hashed participantIdentifier and participantIdentifierScheme combination

Given I am accredited DCP with invalid Client Certificate
When I send POST request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants
And body of request has correct JSON format
Then in response I should get code "403" with error in response

Given I am accredited DCP with valid Client Certificate
When I send POST request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants
And body of request has wrong JSON format
Then in response I should get code "400" with error in response

Given I am accredited DCP with valid Client Certificate
When I send POST request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants
And body of request has correct JSON format with wrong capabilityPublisherID
Then in response I should get code "403" with error in response

Given I am nonaccredited DCP with valid Client Certificate
When I send POST request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants
And body of request has correct JSON format
Then in response I should get code "422" with "DCL-0001" error in response

Given I am accredited DCP with valid Client Certificate
When I send POST request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants
And body of request has correct JSON format with incorrect participantIdentifier
Then in response I should get code "400" with error in response

Given I am accredited DCP with valid Client Certificate
When I send POST request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants
And body of request has correct JSON format with incorrect participantIdentifierScheme
Then in response I should get code "400" with error in response

Given I am accredited DCP with valid Client Certificate
And I know participant which have an active relationship with another DCP
When I send POST request on https://{DCL Domain Name}/api/capabilityPublishers/{capabilityPublisherID}/participants
And body of request has correct JSON format with that participant credentials
Then in response I should get code "400" with error in response
##TODO: error 409 (not in spec)

Given I am accredited DCP with valid Client Certificate
And I know DCL with invalid Server certificate
When I try to establish https connection with that DCL
Then I tear down connection

### Conditions to be covered on Scenarios
# [POST] https://<Digital Capability Locator Domain Name>/api/capabilityPublishers/{capabilityPublisherID}/participants
# TLS 1.2 Mutual (Client and Server) Certificate Authentication
# JSON & XML support
# Error conditions return the corresponding error messages and http status ("201" => "created","400" => "bad request","403" => "Forbidden","404" => "Not found","422" => "Unprocessable entity", "5xx" => "Server Error")
# HTTP 500 level errors return a sanitised error response that does not expose the internal workings or configuration of the DCL.
# request and response examples available under 8.3.1 @ DCL Implementation Guide

# Success: Creating DNS U-NAPTR Record using a hash of the Participant’s Unique Identifier and Issuer, prefixed by ‘b-‘ and suffixed by the Digital Capability Locator’s Domain Name
# If no Relationship Start Date is specified then the relationship will commence on the current date (Canberra Australia).

# The DCP ID should be a valid ID.
# The DCP must have a current status of "Accredited".
# A DCP can only add a participant for their own DCP.
# The participant Identifier must meet the structural format requirements of the identifier scheme.
# The participant identifier scheme must be on the Council's list of approved identifiers, as per the Policy on the use of business identifiers.
# The participant must not have an active relationship with another DCP. If they do then an error must be returned.
