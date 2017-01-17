""" host_from_abn.py

Expects a single command line argument, which is a valid ABN

Prints host returned by a DCL lookup for that ABN.

Uses hardcoded DCL_DOMAIN, which is not the real .gov.au one
(because it doesn't exist yet).
"""
import sys
import util

# hardcoded values
ID_TYPE='ABN'  # the only type currently supported
DCL_DOMAIN="dcl.testpoint.io" # fix this later

# TODO: the argparse thing
# TODO: validate the argument is ABN
try:
    ID = sys.argv[1]
except:
    # you probably forgot to pass a parameter
    sys.exit(1)

# convert ABN into a OASIS-style NAPTR query address
qs = util.dcl_query_string(ID_TYPE, ID, DCL_DOMAIN)
try:
    # this will error if we miss (no result)
    result = util.dns_query(qs)
    print(result)
    sys.exit(0)
except:
    # catch-all error, presumably we had a miss
    # do nothing except exit with non-zero status
    sys.exit(1)
