Feature: Participant monitor and perform health checks on DCL services
    As a participant
    I need to access a public facility
    So that I can monitor and perform health checks on DCL services
# Section 3.6.1 @ "DCL-BusinessRequirements" Document
# ID: 32

Given I am participant
When I go to /healthcheck/ page
Then I see list of systems 
And all of statuses for them are "true"

####### Conditions to be covered on Scenarios #######
# It's public and won't require login
#???# What kind of health checks needed?
#???# What data needs to be moitored
##Suggested direct monitoring:
#Service availability (api endpoints)
#web site features (e.g. participant search)

##Suggested healthcheck page monitoring:
#primary DNS system (route53 - check status via AWS)
#secondary DNS system - Azure (powerdns ok, MySQL slave ok)
#secondary DNS system - Google (powerdns ok, MySQL slave ok)
#back office systems (num workers, num_workers > 0)
#secondary DNS manager (MySQL master ok)
#asp portal (Django server ok, Postgres ok)
#accreditation management tool (Django ok, Postgres ok, vanguard ok)
