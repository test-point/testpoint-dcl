Feature: Accreditation Support Staff member can reactivate suspended or revoked Service Provider's accreditation
    As an Accreditation Support Staff member
    I need to reactivate suspended or revoked Service Provider's accreditation on the Accreditation Management Tool
    So that I keep ASPs records upto date
# Section 3.4.1 @ "DCL-BusinessRequirements" Document
# ID: 41
# User Interface

Given I am authorized Accreditation Support Staff member
And I am at "View Service Providers" page of a "Suspended" Service Provider
Then I should see option to "Reactivate" it's accreditation

Given I am authorized Accreditation Support Staff member
And I am at "View Service Providers" page of a "Suspended" Service Provider
When I choose to "Reactivate" it's accreditation
And enter information to describe the cause of reactivation decission
Then I should see Service Provider status updated to "Accredited"

Given I am authorized Accreditation Support Staff member
And I am at "View Service Provider" page of an "Suspended" Digital Capability Publisher
When I choose to "Reactivate" it's accreditation
And enter information to describe the cause of reactivation decission
Then all participants’ related to this DCP will have their DNS record re-instated, unless it has been superseded by another DCP relationship.


Given I am authorized Accreditation Support Staff member
And I am at "View Service Providers" page of a "Revoked" Service Provider
Then I should see option to "Reactivate" it's accreditation

Given I am authorized Accreditation Support Staff member
And I am at "View Service Providers" page of a "Revoked" Service Provider
When I choose to "Reactivate" it's accreditation
And enter information to describe the cause of reactivation decission
Then I should see Service Provider status updated to "Accredited"

Given I am authorized Accreditation Support Staff member
And I am at "View Service Provider" page of an "Revoked" Digital Capability Publisher
When I choose to "Reactivate" it's accreditation
And enter information to describe the cause of reactivation decission
Then all participants’ related to this DCP will have their DNS record re-instated, unless it has been superseded by another DCP relationship.

####### Conditions to be covered on Scenarios #######
# User authenticated using Username/Password Authentication (integration with Vanguard Federated Authentication Service)
# Only authorized user can access this page
# Action available from view ASP page
# User insert information to support the reactivation decision and provide an enduring audit record.
# When completing the form the Service Provider’s Accreditation status is set to “Accredited”.
# In case of DCP, all participants’ related to this DCP will have their DNS record re-instated, unless it has been superseded by another DCP relationship.
