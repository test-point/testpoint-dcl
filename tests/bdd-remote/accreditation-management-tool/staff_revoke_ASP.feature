Feature: Accreditation Support Staff member can revoke a Service Provider's accreditation in the DCL
    As an Accreditation Support Staff member
    I need to revoke a Service Provider's accreditation on the Accreditation Management Tool
    So that I keep ASPs records upto date
# Section 3.4.1 @ "DCL-BusinessRequirements" Document
# ID: 30
# Special handling of DCP mentioned on story with ID: 40
# User Interface

Given I am authorized Accreditation Support Staff member
And I am at "View Service Providers" page of an "Accredited" Service Provider
Then I should see option to "Revoke" it's accreditation

Given I am authorized Accreditation Support Staff member
And I am at "View Service Providers" page of an "Accredited" Service Provider
When I choose to "Revoke" it's accreditation
And enter information to describe the cause of revoke decission
Then I should see Service Provider status updated to "Revoked"

Given I am authorized Accreditation Support Staff member
And I am at "View Service Provider" page of an "Accredited" Digital Capability Publisher
When I choose to "Revoke" it's accreditation
And enter information to describe the cause of revoke decission
Then all DNS UNAPTR records for participants who have an active relationship with that DCP recorded in the DCL should be removed
And These entries will be replaced by a relationship with the default DCP

####### Conditions to be covered on Scenarios #######
# User authenticated using Username/Password Authentication (integration with Vanguard Federated Authentication Service)
# Only authorized user can access this page
# Action available from view ASP page
# User insert information to support the revocation decision and provide an enduring audit record.
# When completing the form the Service Provider’s Accreditation status is set to “Revoked”.
# In case of DCP, DCL will remove all DNS UNAPTR records for participants who have an active relationship with that DCP recorded in the DCL. These entries will be relaced by a relationship with the default DCP.
