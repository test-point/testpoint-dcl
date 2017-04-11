Feature: Accreditation Support Staff member can modify Service Provider information
    As an Accreditation Support Staff member
    I need to update Service Provider information on the Accreditation Management Tool
    So that I keep updated record for Accredited Service Provider.
# Section 3.4.1 @ "DCL-BusinessRequirements" Document
# ID: 29
# User Interface

Given I am authorized Accreditation Support Staff member
And I am at "List Service Providers" page
When I choose a Service Provider to update
Then I should be redirected to "Edit Service Provider" page

Given I am authorized Accreditation Support Staff member
And I am at "Edit Service Provider" page
Then I should see the same add form populated with this Service Provider data

Given I am authorized Accreditation Support Staff member
And I am at the last step at "Edit Service Provider" page
When I navigate back and forth through the various steps
Then I should see the form keeps data inserted in each step

Given I am authorized Accreditation Support Staff member
And I am at "Edit Service Provider" page
When I modify ABN and Trading Name to the same value of another existing Service Provider
Then I should see validation error message
And the record shouldn't be updated

Given I am authorized Accreditation Support Staff member
And I am at "Edit Service Provider" page
When I delete mandatory information
Then I should see validation error message
And the record shouldn't be updated
####### Conditions to be covered on Scenarios #######
# Form should have all fields of the addition form
# The user should be able to navigate back and forth through the various steps.
# Users can't create duplicate records for a business on the basis of ABN and Trading Name
# Users are required to enter all mandatory information and cannot suspend/resume the process.
# User authenticated using Username/Password Authentication (integration with Vanguard Federated Authentication Service)
# Only authorized user can access this page
