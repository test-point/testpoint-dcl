from envparse import env

# IAM user credentials with minimal permissions: access to create/update records for
# required zone.
# if you leave it empty then you shall pass these credentials somehow else or assume
# they are already set up by some different method
# if you get AWS Credentials error then it's probably the best place to start looking for it
ROUTE_53_IAM_ACCESS_KEY = env("DCL_ROUTE_53_IAM_ACCESS_KEY", default=None)
ROUTE_53_IAM_ACCESS_SECRET = env("DCL_ROUTE_53_IAM_ACCESS_SECRET", default=None)

# Zone id, usually something like Z3J0V63VOKME0Y
# required if Route53 backend is used
ROUTE53_ZONE_ID = env('DCL_ROUTE53_ZONE_ID', default=None)
