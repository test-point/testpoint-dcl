# DCL server
Our implementation of a DNS based capability lookup. The central directory.


## About

This is a HTTP server providing ability to update your NAPTR record in configurable backends (AWS Route53 currently implemented). It's designed to be run behind an HTTPS reverse proxy.

Provided with a target hostname, it sets standard record for given participant ID.

Assumed that participant_id is beling provided by some trusted IdentityProvider. Currently and for test purposes idp.testpoint.io is being used.


## Deployment

These are steps to start local installation of DCL provider or put it somewhere for wide access.

You need some external resources to get it working:
* identity provider - the simplest case is to use idp.testpoint.io, create your own RP and add some synthetic ABN users. All details may be found on it's website.
* AWS credentials. You need api key and secret for some IAM user with access to target Route53 hosted zone. You may use your own user/root credentials, but only locally please and for initial testing and try not to spoil it. Before deploying your project somewhere please make such user.


### Local deployment

Instructions for starting this at *nix machine. Not tested on Windows but should work with perhaps only minor modifications.


#### *nix-based OS

0. Make sure you have requirements installed:

    python2.7 (latest stable tested)
    virtualenv

1. copy any manage.sh.sample to manage.sh and runserver.sh.sample to runserver.sh
    1.1 open manage.sh and fix variables, e.g. your AWS credentials.
    1.2. you might need to create the postgres database; or just uncomment and use sqlite section.

2. `./manage.sh check
    Expected: `System check identified no issues (0 silenced).`
    Some warnings are not good, but okay.

3. `./manage.sh migrate`
   No errors expected.

4. `./manage.sh createsuperuser`

To run the development server please use `./runsever.sh`

Expected result: some console output and url to navigate, 127.0.0.1.

Expected result after navigating the given url: dcl.testpoint.io analogue - blue website.


### Zappa

Our reference service [https://dcl.testpoint.io](https://dcl.testpoint.io) is published on AWS Lambda, behind AWS API Gateway using an orchestration tool called [Zappa](https://github.com/Miserlou/Zappa).


#### Prepare

0. Open Zappa github and have it ready. Good to read and understad the README if you have 10 minutes.
0.1. Select the region you are going to deploy your project; create all objects only in this region (it's important part). Except cross-region things like Cloudfront.
1. find `src/zappa_settings.conf.sample` file, copy it to `src/zappa_settings.conf` and and update the new one to your needs. Details about S3 buckets follow.
2. Create 2 S3 buckets: one for zappa private files and one for public static files. We follow next naming convention: `zappa-{dev|stage|prod}-dcl-testpoint-io[-static]`.
3. Find file `dcl.testpoint.env.json.sample`, copy it to `dcl.testpoint.env.json` and put it into some place where it never leaves your PC except when you upload it to S3 bucket, first private one. `var` directory in root was dedicated to such things. Update it's contents - please note all these zappa files are pure JSON, not Javascript, so any syntax error may be fatal (for example, forgotten comma before `}` character). Remove any comments as well.


#### Zappa deployment

0. Make sure your console applications have access to some AWS credentials: [doc](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-quick-configuration) (or just export `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` variables in this bash session before doing any Zappa - simple solution)
1. Continue to our Zappa Wiki Page (which is universal for all Zappa projects, so it's not fun to copy it everywhere).


## Support

Please raise problems, issues or suggestions as tickets at GitHub, or talk to us at the AusDigital community site (https://talk.ausdigital.org/)

