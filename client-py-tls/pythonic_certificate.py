#!/usr/bin/env python
# http://nategood.com/client-side-certificate-authentication-in-ngi#
import pprint

import requests


resp = requests.get(
    'https://dcl-hostname/api/v0/demo_auth/',
    cert=('./client.crt', './client.key'),
    verify=False
)

print(resp.status_code)
pprint.pprint(resp.json())
