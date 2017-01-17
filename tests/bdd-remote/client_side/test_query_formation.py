""" test_query_formation.py

Before we can test the server-side implementation, we nee to ensure our
client-side is capable of sending well formed requests.

well_formed_dns_query_string.feature demonstrates the goal.

This depends on hesdigest_of_md5_hash and urn_encoded_identifiers,
combined correctly as hexdigest_of_urn_encoded_identifiers
"""
from pytest_bdd import (
    scenarios,
    given,
    scenario,
    then,
    when,
    parsers
)
import util

scenarios('.')

@given(parsers.parse('I have string {foo}'))
def foo_string(foo):
    print(foo)
    return dict(string=foo, hash=None)

@when('I calculate MD5 hexdigest of string')
def calculate_md5_hexdigest_of_foo(foo_string):
    foo_string['hash'] = util.md5_hexdigest(
        foo_string['string'])

@then(parsers.parse('I get hashed value of string {hexdigest}'))
def get_hexdigest_of_foo(foo_string, hexdigest):
    assert foo_string['hash'].upper() == hexdigest.upper()

@given(parsers.parse('I know a business has the identifier {identifier}'))
def business_identifier(identifier):
    return dict(
        identifier=identifier,
        id_scheme=None,
        urn=None,
        urn_hexdigest=None,
        dcl_domain=None,
        dcl_query=None)

@given(parsers.parse('I know the identifier type is {scheme}'))
def know_the_identifier_type_is_id_scheme(business_identifier, scheme):
    business_identifier['id_scheme']=scheme

@given(parsers.parse('the DCL domain name is {domain}'))
def the_dcl_domain_name_is_dcl_domain(business_identifier, domain):
    business_identifier['dcl_domain'] = domain

@when('I calculate NID format identifier')
def calculate_nid_format_identifier(business_identifier):
    # TODO: clarify requirements around other supported codes
    urn_template = '{}:{}::{}'
    id_scheme = business_identifier['id_scheme']
    identifier = business_identifier['identifier']
    if id_scheme not in util.ISO6523_CODES.keys():
        raise Exception('type {} not in util.ISO6550_CODES {}'.format(
            id_scheme, str(util.ISO6523_CODES)))
    if not identifier:
        raise Exception('unable to calculate NIR format identifier on None identifier')
    else:
        business_identifier['urn'] = urn_template.format(
            util.NID_PREFIX,
            util.ISO6523_CODES[id_scheme],
            identifier)

@when('I calculate the DNS query string')
def calculate_the_dns_query_string(business_identifier):
    template = "b-{}.{}"
    if not business_identifier['urn_hexdigest']:
        calculate_the_md5_hexdigest_of_the_nid_format_identifier(business_identifier)
    business_identifier['dcl_query'] = template.format(
        business_identifier['urn_hexdigest'],
        business_identifier['dcl_domain'])

@when('I calculate the MD5 hexdigest of the NID format identifier')
def calculate_the_md5_hexdigest_of_the_nid_format_identifier(business_identifier):
    if not business_identifier['urn']:
        calculate_nid_format_identifier(business_identifier)
    business_identifier['urn_hexdigest'] = util.md5_hexdigest(
        business_identifier['urn'])

@then(parsers.parse('I get the URN {urn}'))
def i_get_the_urn_valid_urn_of_identifier(business_identifier, urn):
    # case-insensitive comparison
    assert urn.upper() == business_identifier['urn'].upper()

@then(parsers.parse('I get the address {expected}'))
def i_get_the_address_calculated(business_identifier, expected):
    found = business_identifier['dcl_query']
    if not found:
        calculate_the_dns_query_string(business_identifier)
        found = business_identifier['dcl_query']
    # case insensitive comparison
    assert found.upper() == expected.upper()

@then(parsers.parse('I get the value {expected}'))
def value_valid_md5_hexdigest_of_urn(business_identifier, expected):
    assert expected.upper() == business_identifier['urn_hexdigest'].upper()
