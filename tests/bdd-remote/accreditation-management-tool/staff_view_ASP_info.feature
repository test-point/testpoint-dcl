Feature: Accreditation Support Staff member can view Accredited Service Provider information
    As an Accreditation Support Staff member
    I need to view Accredited Service Provider information on the Accreditation Management Tool
    So that I can review it and take further actions like updating its status
# Section 3.4.1 @ "DCL-BusinessRequirements" Document
# @mentioned on Revoke Story with # ID: 30
# @mentioned on Suspend Story with # ID: 31
# User Interface

Given I am authorized Accreditation Support Staff member
And I am at "List Service Providers" page
When I select a Service Provider
Then I should see all his inserted information

####### Conditions to be covered on Scenarios #######
# User authenticated using Username/Password Authentication (integration with Vanguard Federated Authentication Service)
# Only authorized user can access this page
# User can view all available information of ASP
