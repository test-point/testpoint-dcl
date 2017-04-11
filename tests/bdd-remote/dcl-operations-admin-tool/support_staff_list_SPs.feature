Feature: DCL Operations Support Staff member can list all participants or Service Providers
    As a DCL Operations Support Staff member
    I need to list all participants or Service Providers on the DCL Operations Admin Tool
    So that I can support the DCL as per standard operating procedures.
# Section 3.6.1 @ "DCL-BusinessRequirements" Document
# @mentioned on Story with # ID: 22
# User Interface

Given I am authorized DCL Operations Support Staff member
When I am at "Service Providers" page
Then I should see list of all Service Providers showing  Service Provider ID, Trading Name, accreditation status.

Given I am authorized DCL Operations Support Staff member
When I am at "Service Providers" page
Then I should be able to navigate through pages

Given I am authorized DCL Operations Support Staff member
When I am at "Service Providers" page
Then I should be able to search specific record

####### Conditions to be covered on Scenarios #######
# User authenticated using
# Only authorized user can access this page
# User can view list of participants and ASPs
# List should be paginated
# Only record main information should be displayed like ABN, Trading name and status
# User can search records
