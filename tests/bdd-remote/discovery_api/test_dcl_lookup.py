""" test dcl_lookup.py

These tests assume the DCL has hardcoded fxtures.

TODO: push fixtures to environment variables (override)
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
import fixtures

FIXTURE_SIZE = 5

scenarios('.')

def query_dcl_fixture_idx(load_fixtures, idx):
    if idx not in range(0, FIXTURE_SIZE):
        raise Exception("idx {} out of expected range".format(idx))
    e = load_fixtures[idx]
    e['found'] = util.dns_query(
        util.dcl_query_string(
            e['id_scheme'],
            e['identifier'],
            e['dcl_domain']))

def check_result(load_fixtures, idx):
    if idx not in range(0, FIXTURE_SIZE):
        raise Exception("idx {} out of expected range".format(idx))
    e = load_fixtures[idx]
    assert e['found'] == e['expected']


@given('I know a DCL with expected lookup values')
def load_fixtures():
    return fixtures.VALUES
#
# these are unrolled to avoid nasty exec-style code
#
@when('I query the DCL for the first lookup fixture')
def first_lookup_fixture(load_fixtures):
    query_dcl_fixture_idx(load_fixtures, 0)

@when('I query the DCL for the second lookup fixture')
def second_lookup_fixture(load_fixtures):
    query_dcl_fixture_idx(load_fixtures, 1)

@when('I query the DCL for the third lookup fixture')
def third_lookup_fixture(load_fixtures):
    query_dcl_fixture_idx(load_fixtures, 2)

@when('I query the DCL for the fourth lookup fixture')
def fourth_lookup_fixture(load_fixtures):
    query_dcl_fixture_idx(load_fixtures, 3)

@when('I query the DCL for the fifth lookup fixture')
def fifth_lookup_fixture(load_fixtures):
    query_dcl_fixture_idx(load_fixtures, 4)

@then('the results match the first lookup fixture expected value')
def first_check_result(load_fixtures):
    check_result(load_fixtures, 0)

@then('the results match the second lookup fixture expected value')
def second_check_result(load_fixtures):
    check_result(load_fixtures, 1)

@then('the results match the third lookup fixture expected value')
def third_check_result(load_fixtures):
    check_result(load_fixtures, 2)

@then('the results match the fourth lookup fixture expected value')
def fourth_check_result(load_fixtures):
    check_result(load_fixtures, 3)

@then('the results match the fifth lookup fixture expected value')
def fifth_check_result(load_fixtures):
    check_result(load_fixtures, 4)
