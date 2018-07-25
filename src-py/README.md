# DCL server

Our implementation of a DNS based capability lookup. The central directory. Feel free to contact us at https://chat.ausdigital.org/ if you are having any problems.


## About

This is a Web Service providing ability to update your NAPTR record in configurable backends (AWS Route53 currently implemented). It's designed to be run behind an HTTPS reverse proxy for extra security, but no need of such complications for demo/development purposes.

Provided with a target hostname, it sets standard record for given participant ID.

Assumed that participant_id is beling provided by some trusted IdentityProvider. Currently and for test purposes idp.testpoint.io is being used.


## Deployment

These are steps to start local installation of DCL provider or put it somewhere for wide access.

You need some external resources to get it working:
* identity provider - the simplest case is to use idp.testpoint.io, create your own RP and add some synthetic ABN users. All details may be found there.
* AWS credentials. You need api key and secret for some IAM user with access to target Route53 hosted zone. You may use your own user/root credentials, but only locally please and for initial testing and try not to spoil it. Before deploying your project somewhere please make such user.


### Local deployment

Instructions for starting this at `*nix` machine. Not tested on Windows but should work with perhaps only minor modifications.


#### Unix-based OS (Linux, Macos)

0. Make sure you have requirements installed:

    python2.7 (latest stable tested) - python3 is not supported yet!
    virtualenv

1. copy `manage.sh.sample` file to `manage.sh`
    1.1 open `manage.sh` and update variables content, e.g. your AWS credentials and IDP keys/secrets
    1.2. configure the database. For real usage it's advised to use postgres, for local/demo it's enough to leave default SQLite values.

2. `./manage.sh check`
    Expected: `System check identified no issues (0 silenced).`
    Some warnings are not good, but okay.

3. `./manage.sh migrate`
   No errors expected, some output about tables creation will be given.

4. `./manage.sh createsuperuser` - optional.

To run the development server please use `./manage.sh runserver`

Expected result: some console output and url to navigate. Url is going be look like `http://127.0.0.1:8000`. Now you must ensure that you use exactly the same IP and port as your `manage.sh` file `DCL_HOSTNAME` setting.

Expected result after navigating the given url: dcl.testpoint.io analogue - blue website, which will redirect you to the IDP login page, which will ask you for some IDP username/password (check idp.testpoint.io for details about user creation). Then it will ask you for authorisation - to allow your fresh DCL installation to see base details about that IDP user (as typical social auth works). And then you'll be redirected back to your DCL installation, where the blue website will be serving you.


#### IDP configuration

You need some IDP to be configured and accepting auth requests from your fresh DCL service. Please feel free to use idp.testpoint.io. To configure it:

* navigate to idp.testpoint.io and find the login link
* login using github
* go to "RP (relaying parties)" section
* create some RP:
  * leave client type "Confidential"
  * Response type: "code" (there are variants, but "code" is a safe choice)
  * leave `JWT Algorithm` intact, RS256 suits the best
  * Redirect URIs: add lines like `http://127.0.0.1:8000/oidc/authz/` for each domain which you are about to use. In simple local development case only this line is enough.

If you are getting error `Redirect URI Error The request fails due to a missing, invalid, or mismatching redirection URI (redirect_uri).` then your local DCL installation sends some wrong url to the IDP. Please find which one (get the value of the parameter redirect_uri to the page where you see that error) and update "Redirect URIs" field on IDP accordingly.


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


### Classic deployment

For classic deployment we are going to use Nginx as web server and gunicorn for run backend Python code; it's assumed to be run on some docker containers at some EC2 box or any other hosting.

* ensure you have access to Route53 zone and you have made the domain name for your installations (example: `some-dcl.testpoint.io`).
* get AWS credentials (access key and secret) with access to Route53 management only
* put these credentials to .env files (examples provided)
* deploy the source code with env file at same level as docker-compose file to some service
* run docker-compose up (or docker-compose up -d to run it in background)
* configure Nginx to pass requests to some port, which is available from docker-compose file
* configure Nginx to support HTTPS and desired domain name
* make sure you can run `manage.py collectstatic --noinput` and make the resulting directory available as http://your-host/static/

Please note that nginx needs to support mutual TLS auth as described http://nategood.com/client-side-certificate-authentication-in-ngi here and as exampled in `../client_py_tls` folder.

## Support

Please raise problems, issues or suggestions as tickets at GitHub, or talk to us at the AusDigital community site (https://ausdigital.org/)
