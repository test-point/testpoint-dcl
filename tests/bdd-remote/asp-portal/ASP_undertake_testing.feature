Feature: Accredited Service Provider can undertake interoperability testing
    As an Accredited(Inc. provisional) Service Provider
    I need to undertake interoperability testing with other ASPs using the DCL.
    So that I can validate system enhancements or wanted to become accredited.
# Section 3.7.1 @ "DCL-BusinessRequirements" Document
# ID: 21, ID: 33

Given I am Accredited Service Provider
And there is isolated interoperability testing enviroment with URI
Wnen I allocate testing identities in the interoperability testing environment
Then I am able to undertake interoperability testing

Given I am Accredited Service Provider
And there is isolated interoperability testing enviroment with URI
Wnen I am logged into the interoperability testing environment
Then I am not able to product digital certificates

####### Conditions to be covered on Scenarios #######
# An independent, isolated duplicate of the DCL will be available to support service providers to undertake interoperability and end-to-end testing.
# This solution will not contain production digital certificates for any service provider.
# This solution will have a URI which clearly identifies it and all its participant records as belonging to the test environment.
# Service provider allocate testing identities in the interoperability testing environment.
