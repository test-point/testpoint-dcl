Feature: Accredited Service Provider verify the status of another service provider.
    As an Accredited Service Provider
    I need to verify the status and identity of another service provider
    so that I can confirm his status and his identity
# Section 3.3.1 @ "DCL-BusinessRequirements" Document
# ID: 18
# ID: 23
# Section 8.4.2 & 8.4.3 @ "DCL Implementation Guide" Document
# REST API

Given I am Accredited Service Provider
When I send GET request to https://<DCL Domain>/api/v1/capabilityPublishers?id={dcp_id} with existindg DCP ID
Then in response I get "200" status code
And response body structure is in correct JSON format
And response contains of specific DCP's ID, Trading Name, Accreditation Status

Given I am Accredited Service Provider
When I send GET request to https://<DCL Domain>/api/v1/capabilityPublishers?id={dcp_id} with nonexisting DCP ID
Then in response I get "404" status code
And response contains error code,name, userMessage

Given I am Accredited Service Provider
When I send GET request to https://<DCL Domain>/api/v1/capabilityPublishers?name={dcp_name} with existing DCP Name
Then in response I get "200" status code
And response body structure is in correct JSON format
And response contains of specific DCP's ID, Trading Name, Accreditation Status

Given I am Accredited Service Provider
When I send GET request to https://<DCL Domain>/api/v1/capabilityPublishers?name={dcp_name_with_wildcard} with part of existing DCP Name
Then in response I get "200" status code
And response body structure is in correct JSON format
And response contains all DCP's records having name that fits wildcard search

Given I am Accredited Service Provider
When I send GET request to https://<DCL Domain>/api/v1/accessPoints?id={ap_id} with existindg Access Point ID
Then in response I get "200" status code
And response body structure is in correct JSON format
And response contains of specific Access Point's ID, Trading Name, Accreditation Status

Given I am Accredited Service Provider
When I send GET request to https://<DCL Domain>/api/v1/accessPoints?id={ap_id} with nonexisting Access Point ID
Then in response I get "404" status code
And response contains error code,name, userMessage

Given I am Accredited Service Provider
When I send GET request to https://<DCL Domain>/api/v1/accessPoints?name={ap_name} with existing Access Point Name
Then in response I get "200" status code
And response body structure is in correct JSON format
And response contains of specific Access Point's ID, Trading Name, Accreditation Status

Given I am Accredited Service Provider
When I send GET request to https://<DCL Domain>/api/v1/accessPoints?name={ap_name_with_wildcard} with part of existing Access Point Name
Then in response I get "200" status code
And response body structure is in correct JSON format
And response contains all Access Point's records having name that fits wildcard search

####### Conditions to be covered on Scenarios #######
# ASP can invoke an API to determine if a service provider is on the accreditation whitelist and their associated the Mutual TLS Certificate chain.
# Two certificate chains may be returned to support seamless transition upon certificate expiry.
# ASP can lookup another provider's status using either of Service provider ID, Trading Name
# URL: [GET] ** these urls are suggested and not explicity mentioned in the document
    # * https://<DCL Domain>/api/v1/capabilityPublisher?id=25
    # * https://<DCL Domain>/api/v1/capabilityPublisher?name=xyz
    # * https://<DCL Domain>/api/v1/accessPoint?id=25
    # * https://<DCL Domain>/api/v1/accessPoint?name=xyz
# search by name should be wildcard search not exact match
# Success response should contain Service provider ID, Trading Name, Accreditation Status
# Support JSON & XML (JSON by default)
# Return 404 if the provider record cannot be found
# Return appropriate status code (200,400,5xx)
# Failure response should contain errors records  with (code,name, userMessage) for each error record
