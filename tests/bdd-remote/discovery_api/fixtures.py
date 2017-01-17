""" test dcl_lookup.py

These tests assume the DCL has 5 stable/known records.
"""
from envparse import env

VALUES = (
    {
        'found':None,
        'dcl_domain': env('DCL_READ_DOMAIN', default='dcl.testpoint.io'),
        'id_scheme': env('DCL_TEST_EG1_SCHEME', default='ABN'),
        'identifier': env('DCL_TEST_EG1_IDENTIFIER', default='33767197359'),
        'expected': env('DCL_TEST_EG1_CNAME', default='smp.testpoint.io.')
    },{
        'found':None,
        'dcl_domain': env('DCL_READ_DOMAIN', default='dcl.testpoint.io'),
        'id_scheme': env('DCL_TEST_EG2_SCHEME', default='ABN'),
        'identifier': env('DCL_TEST_EG1_IDENTIFIER', default='14247983785'),
        'expected': env('DCL_TEST_EG2_CNAME', default='smp.testpoint.io.')
    },{
        'found':None,
        'dcl_domain': env('DCL_READ_DOMAIN', default='dcl.testpoint.io'),
        'id_scheme': env('DCL_TEST_EG3_SCHEME', default='ABN'),
        'identifier': env('DCL_TEST_EG3_IDENTIFIER', default='67008125522'),
        'expected': env('DCL_TEST_EG3_CNAME', default='smp.testpoint.io.')
    },{
        'found':None,
        'dcl_domain': env('DCL_READ_DOMAIN', default='dcl.testpoint.io'),
        'id_scheme': env('DCL_TEST_EG4_SCHEME', default='ABN'),
        'identifier': env('DCL_TEST_EG4_IDENTIFIER', default='76031101072'),
        'expected': env('DCL_TEST_EG4_CNAME', default='smp.testpoint.io.')
    },{
        'found':None,
        'dcl_domain': env('DCL_READ_DOMAIN', default='dcl.testpoint.io'),
        'id_scheme': env('DCL_TEST_EG5_SCHEME', default='ABN'),
        'identifier': env('DCL_TEST_EG5_IDENTIFIER', default='17102364628'),
        'expected': env('DCL_TEST_EG5_CNAME', default='smp.testpoint.io.')
    },)
