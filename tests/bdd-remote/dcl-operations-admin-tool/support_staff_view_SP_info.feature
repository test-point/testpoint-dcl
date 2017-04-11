Feature: DCL Operations Support Staff member can view participant or Service Provider information
    As a DCL Operations Support Staff member
    I need to view Service Provider information on the DCL Operations Admin Tool
    So that I can review it and manually correct data if needed
# Section 3.6.1 @ "DCL-BusinessRequirements" Document
# @mentioned on Story with # ID: 22
# User Interface

Given I am authorized DCL Operations Support Staff member
When I am at "Service Providers" page
Then I should see list of all Service Providers showing  Service Provider ID, Trading Name, accreditation status.

Given I am authorized DCL Operations Support Staff member
When I am at "Service Providers" page
Then I should be able to view information of specific Service Provider such as Service Provider ID, Trading Name, Contact Email, URL (for registration page), Accreditation status, Digital Certificates.

####### Conditions to be covered on Scenarios #######
# User authenticated using
# Only authorized user can access this page
# User can view all available information of participant or ASP
