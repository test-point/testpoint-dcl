Feature: DCL Operations Support Staff member can modify participant or Service Providerinformation
    As a DCL Operations Support Staff member
    I need to update participant or Service Provider information on the DCL Operations Admin Tool
    So that I can support the DCL as per standard operating procedures.
# Section 3.6.1 @ "DCL-BusinessRequirements" Document
# ID: 22
# User Interface

Given I am authorized DCL Operations Support Staff member
When I am at "Service Providers" page
Then I should see list of all Service Providers showing  Service Provider ID, Trading Name, accreditation status.

Given I am authorized DCL Operations Support Staff member
When I am at page of specific Service Provider
Then I should be able to modify key information such as metadata,Certificates, Addresses, Nominated Contact Points.

Given I am authorized DCL Operations Support Staff member
When I change key information of specific Service Provider
And I save those changes
And I am at page of specific Service Provider
Then I should be able to see changed information.

####### Conditions to be covered on Scenarios #######
# User can edit only key information
# User authenticated using
# Only authorized user can access this page
