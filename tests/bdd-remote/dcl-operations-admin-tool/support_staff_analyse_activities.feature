Feature: DCL Operations Support Staff member see reports that analyse DCL activities
    As a DCL Operations Support Staff member
    I need to have see reports for DCL activities on the DCL Operations Admin Tool
    So that I can analyse DCL activities and be able to build and save queries

# Section 3.6.1 @ "DCL-BusinessRequirements" Document
# ID: 25
# User Interface

Given I am authorized DCL Operations Support Staff member
When I am at "Participants history" page of an OPS Tool
Then I should see list of DCL records history items
And I should be able to filter the list by "Participant ID"
And I should be able to save filter state

Given I am authorized DCL Operations Support Staff member
When I am at "Participants history" page of an OPS Tool
Then I should see list of DCL records history items
And I should be able to filter the list by "Event date"
And I should be able to save filter state

Given I am authorized DCL Operations Support Staff member
When I am at "ASP history" page of an OPS Tool
Then I should see list of ASP history events
And I should be able to filter the list by "Event date"
And I should be able to save filter state

####### Conditions to be covered on Scenarios #######
#???# User authenticated using
# Only authorized user can access this page
# Audit history for participants;
# Audit history for Accredited Service Providers;
# Audit history for a specified day or time period;
#???# What kind of records to be audited, how it'll be stored and how it'll be displayed
