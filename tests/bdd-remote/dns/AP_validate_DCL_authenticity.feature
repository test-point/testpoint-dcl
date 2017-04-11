Feature: Access Point validate the Authenticity of the DCL
    As an Access Point
    I need to validate the Authenticity of the DCL
    So that I determine that information has been provided by the DCL and not an unauthorised third-party.

# Section 3.1.1 & 3.2.1 @ "DCL-BusinessRequirements" Document
# ID: 24
#

Given I am Access Point
And I know DCL DNS name
When I lookup DCL DNS name in a list of agreed domain names
Then record is present in list

Given I am Access Point
And I know DCL DNS name
When I lookup DNS Ownership records
Then there is reflection of relationship between the DNS name and a well known entity (Digital Business Council or ATO)

Given I am Access Point
And I know DCL DNS name
When I request TLS certificate from given DCL name
Then there is valid certificate issued by a reputable Certificate Authority
And Common Name references to DCL’s domain name

### Conditions to be covered on Scenarios

# The DCL DNS is exposed under an agreed domain name;
# DNS Ownership records must clearly reflect the relationship between the DNS name and a well known entity. Eg. Digital Business Council or ATO.
# In relation to all other DCL lookup and maintenance services, TLS 1.2 must be used and the certificate must be issued by a reputable Certificate Authority and the Common Name must reference the DCL’s well known, fully qualified domain name.
