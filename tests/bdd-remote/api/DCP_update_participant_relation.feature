Feature: Digital Capability Publisher update a participant record to point to his DCP
    As a Digital Capability Publisher
    I need to update a participant record to point to my DCP
    So that a business can seamlessly transition between service providers

# > Subject to agreement on Business Process by the DCL Working Group.

# Section 3.2.1 @ "DCL-BusinessRequirements" Document
# ID: 20
# REST/JSON or REST/XML API

### Conditions to be covered on Scenarios

# A gaining DCP must pre notify the losing DCP of the transition and submit the confirmation/acknowledgement with the update request to the DCL
# The existing relationship is not deleted, but rather end-dated.
# The update request can submit a future date time for the update to take effect so long as it is less that 30 days from the original notification to the existing DCP.
# TLS 1.2 Mutual (Client and Server) Certificate Authentication
