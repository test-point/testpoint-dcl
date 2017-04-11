Feature: Accreditation Support Staff member can list all Accredited Service Providers
    As an Accreditation Support Staff member
    I need to list all Accredited Service Providers on the Accreditation Management Tool
    So that I can maintain them
# Section 3.4.1 @ "DCL-BusinessRequirements" Document
# @mentioned on Update Story with # ID: 29
# Filtratioin @mentioned on Reactivate Story with # ID: 41
# User Interface

Given I am authorized Accreditation Support Staff member
And I am at "List Service Providers" page
Then I should see list of all Accredited Service Providers showing ABN, Trading name and status

Given I am authorized Accreditation Support Staff member
And I am at "List Service Providers" page
Then I should be able to navigate through pages

Given I am authorized Accreditation Support Staff member
And I am at "List Service Providers" page
Then I should be able to filter the list by status

####### Conditions to be covered on Scenarios #######
# User authenticated using Username/Password Authentication (integration with Vanguard Federated Authentication Service)
# Only authorized user can access this page
# User can view list of ASPs
# List should be paginated
# Only ASP main information should be displayed like ABN, Trading name and status
# User can filter list to see only "Revoked" and "Suspended" statuses
# [Nice to Have] List should be filtered by one or more status
