""" util.py

functions for sending a well formed DCL request
"""
import hashlib
import dns.resolver

NID_PREFIX = 'urn:oasis:names:tc:ecore:partyid-type:iso6523'
# TODO: what other schemes do we need to support?
ISO6523_CODES = {'ABN':'0151'}


def md5_hexdigest(string):
    """ returns hexdigest of the md5 hash of a string

    Assumes the canonical form is:
     * lower case
     * utf-8 encoded

    This may or may not be correct, clarification required.
    """
    return hashlib.md5(
        string.lower().encode('utf-8')
    ).hexdigest()

# if more than NID schemes are supported, we might want to have
# another parameter (default=NID) for selecting the appropriate
# prefix, encoding format etc.
def urn_of_identifier(id_scheme, identifier):
    """ return NID format urn of identifier """
    if id_scheme not in ISO6523_CODES.keys():
        msg = 'type {} not in ISO6523_CODES {}'.format(
            id_scheme, str(ISO6523_CODES))
        raise Exception(msg)
    else:
        template = "{}:{}::{}"
        return template.format(
            NID_PREFIX,
            ISO6523_CODES[id_scheme],
            identifier)

# if more than NID schemes, will also require the prefix param
def dcl_query_string(id_scheme, identifier, dcl_domain):
    """ return dcl query string """
    template = "b-{}.{}"
    return template.format(
        md5_hexdigest(urn_of_identifier(id_scheme, identifier)),
        dcl_domain)


def dns_query(query_string):
    """ returnst highest ranking U-NAPTR record for query string

    A NAPTR query may return multiple results. Per RFC 2915, the
    lowest valued "preference" has presedence over higher values.
    Where multiple rules have the same preference, the lowest
    "order" has precedence over higher values.
    """
    results = dns.resolver.query(query_string, 'NAPTR')
    min_preference = None
    min_order_at_min_preference = None
    precedent_service = None  # the CNAME with precedence
    for rdata in results:
        pref = rdata.preference
        order= rdata.order
        value = str(rdata.replacement)
        # TODO: U-NAPTR validation here
        if not min_preference:
            # first record we see is best, at first
            min_preference = pref
            min_order_at_min_pref = order
            precedent_service = value
        elif pref < min_preference:
            # trump on preference
            min_preference = pref
            min_order_at_min_pref = order
            precedent_service = value
        elif pref == min_preference and order < min_order_at_min_pref:
            # trump on order
            min_preference = pref
            min_order_at_min_pref = order
            precedent_service = value
    if precedent_service:
        return precedent_service
    else:
        # raising an exception is probably the wrong thing to do
        raise Exception('No valid NAPTR record found')
