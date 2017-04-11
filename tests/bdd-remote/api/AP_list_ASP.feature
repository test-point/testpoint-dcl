Feature: Access Point list Accredited Service Provider Information
    As an Access Point
    I need to lookup Accredited Service Provider Information
    So that I can discover all accredited Access Points, determine the accreditation status of a particular Access Point or determine a DCP to use
# Section 3.3.1 @ "DCL-BusinessRequirements" Document
# ID: 27
# Section 8.4.2 & 8.4.3 @ "DCL Implementation Guide" Document
# Usecases @ Appendix A @ "DCL Implementation Guide" Document
    # * SUC018 List of Accredited Access Points
    # * SUC019 List of Accredited Digital Capability Publishers
# REST API

Given I am Access Point
When I send GET request with "Accept application/json" header to https://<DCL Domain>/api/v1/capabilityPublisher?limit=25&offset=50
Then in response I get "200" status code
And response body structure is in correct JSON format
And responce contains Accredited DCP's from 50th to 75th

Given I am Access Point
When I send GET request with  with "Accept application/xml" header to https://<DCL Domain>/api/v1/capabilityPublisher?limit=25&offset=50
Then in response I get "200" status code
And response body structure is in correct XML format
And responce contains Accredited DCP's from 50th to 75th

#What are conditions for error 400?

Given I am Access Point
When I send GET request with "Accept application/json" header to https://<DCL Domain>/api/v1/accessPoint?limit=25&offset=50
Then in response I get "200" status code
And response body structure is in correct JSON format
And responce contains Accredited Access Points from 50th to 75th

Given I am Access Point
When I send GET request with "Accept application/xml" header to https://<DCL Domain>/api/v1/accessPoint?limit=25&offset=50
Then in response I get "200" status code
And response body structure is in correct XML format
And responce contains Accredited Access Points from 50th to 75th

####### Conditions to be covered on Scenarios #######
# Only service provider results with a current status of "Accredited" are returned not pending, suspended, revoked or cancelled.
# URL: [GET]
    # * https://<DCL Domain>/api/v1/capabilityPublisher?limit=25&offset=50
    # * https://<DCL Domain>/api/v1/accessPoint?limit=25&offset=50
# Support JSON & XML (JSON by default)
# Return appropriate status code (200,400,5xx)
# Success response should be as mentioned in section 8.4.2.8 in "DCL Implementation Guide" for both XML and JSON
# Failure response should contain errors records  with (code,name, userMessage) for each error record
