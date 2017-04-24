Feature: Accredited Service Provider get the cache details and maximum cache time for ASP lookup information
    As an Accredited Service Provider
    I need to know the cache details and maximum cache time for ASP lookup information
    So that I can enable performant processing workflows.
# Section 3.3.1 @ "DCL-BusinessRequirements" Document
# ID: 37
# Section 8.4.2 & 8.4.3 @ "DCL Implementation Guide" Document

Given I am Accredited Service Provider
When I send GET request to https://<DCL Domain>/api/v1/capabilityPublishers?id={dcp_id} with existindg DCP ID
Then in response I get "200" status code with "Cache-Control" header
And "max-age" directive is defined in that header 

Given I am Accredited Service Provider
When I send GET request to https://<DCL Domain>/api/v1/capabilityPublishers?id={dcp_id} with existindg DCP ID
And request contains "Cache-Control" header with "no-cache" directive
Then in response I get "200" status code with correct respons body
And response body contains non-cached record

Given I am Accredited Service Provider
When I send GET request to https://<DCL Domain>/api/v1/accessPoints?id={ap_id} with existindg Access Point ID
Then in response I get "200" status code with "Cache-Control" header
And "max-age" directive is defined in that header

Given I am Accredited Service Provider
When I send GET request to https://<DCL Domain>/api/v1/accessPoints?id={ap_id} with existindg Access Point ID
And request contains "Cache-Control" header with "no-cache" directive
Then in response I get "200" status code with correct respons body
And response body contains non-cached record

####### Conditions to be covered on Scenarios #######
# All DCL lookup services must provide header information that specifies the maximum cache period.
# All DCL lookup service must allow the requestor to specify cache override behaviour.
# Must use standard HTTP headers.
