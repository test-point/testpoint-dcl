Feature: Accreditation Support Staff member can add Service Provider information into the DCL
    As an Accreditation Support Staff member
    I need to add Service Provider information into the DCL on the Accreditation Management Tool
    So that I keep record for a new Accredited or Provisionally Accredited Service Provider.
# Section 3.4.1 @ "DCL-BusinessRequirements" Document
# ID: 28
# Public fields mentioned on Story with ID: 38
# User Interface

Given I am authorized Accreditation Support Staff member
And I am at "Add Service Provider" page
When I enter all information
Then I should be redirected to "List Service Providers" page
And I find the new record added with all inserted information

Given I am authorized Accreditation Support Staff member
And I am at "Add Service Provider" page
When I enter all information
Then the new record should have "Accredited" status by default

Given I am authorized Accreditation Support Staff member
And I am at the last step at "Add Service Provider" page
When I navigate back and forth through the various steps
Then I should see the form keeps data inserted in each step

Given I am authorized Accreditation Support Staff member
And I am at "Add Service Provider" page
When I enter duplicate ABN and Trading Name
Then I should see validation error message
And the record shouldn't be added

Given I am authorized Accreditation Support Staff member
And I am at "Add Service Provider" page
When I don't enter mandatory information
Then I should see validation error message
And the record shouldn't be added

####### Conditions to be covered on Scenarios #######
# Form fields [Public]
    # Certificates:
        # o Client Certificates
        # o Server Certificates
    # Addresses:
        # o Physical Address;
        # o Website
        # o Contact Email
    # Nominated Contact Points:
        # • Contact Name
        # • Position Title
        # • Contact Email
        # • Phone Number
#???# What is the restricted form fields of the addition form
# The user should be able to navigate back and forth through the various steps.
# Users can't create duplicate records for a business on the basis of ABN and Trading Name
# Users are required to enter all mandatory information and cannot suspend/resume the process.
# User authenticated using Username/Password Authentication (integration with Vanguard Federated Authentication Service)
# Only authorized user can access this page
# New record will have status "Accredited" by default
