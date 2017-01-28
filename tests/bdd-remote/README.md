# Testing the DCL

The code in this directory will test a remote DCL implementation.


## Install

This suite uses python to access (and test) remote DCL, through HTTPS and DNS protocols.
It's developed with python 2.7, other versions may work but are not tested. The python code is tested in Linux and OSX. Raise an issue in https://github.com/test-point/testpoint-dcl if you encounter issues with other python versions or operating systems.

The `test.sh` script will install required python packagess. For it to succeed, the only dependencies you need to have is the `pip` and `virtualenv`.

The HTTPS implementation requires phantomjs, so you will also need that. Note, the Ubuntu OS packaged versons of phantomjs is known NOT to work, instead `npm` installed version. To do this in ubuntu, first install npm and nodejs-legacy, then use npm to install phantomjs-prebuilt:

```
$ apt-get install -y nodejs-legacy npm
$ npm install -g phantomjs-prebuilt
```

## Configuration

The software will evaluate the dcl.testpoint.io target, unless you don't override
this behavior by setting appropriate environment varialbes. 

There is a configuration file mechanism for setting the environment variables in a
convenient way. If `test/config.sh` exists, any variables it exports will be set in
the test runner's environment.

To customise the test target:
 1. `cp config.sh.sample config.sh`
 2. edit `config.sh` to reffer to your chosen target
 3. run the `test.sh` script as usual.

config.sh.sample contains all the variables that the test suite currently uses, with some
documentation of their purpose. The values of these variables in this file are equivalent
to the default values (including this file as-is has no actual effect).

note: `config.sh` is excluded from the repository (`.gitignore`). Your local configuration will not be overwritten by updates.


### Warning: Concurrent use of `DCL_TEST_USER`

If multiple people are running the test suite in parallel with the same `DCL_TEST_USER`, it's
possible the  tests will collide (causing false results). If that's an issue for you,
it's advisable to reserve your own test accounts and use them exclusively.

If you are running against dcl.testpoint.io, you can claim ABNs for exclusive use on
https://idp.testpoint.io/. Log in with a developer account (GitHub user) to manage your
own collection of ABNs, create new ABN and try to login manually from https://dcl.testpoint.io/login/ with  newly created credential to ensure it works.


## Running the test suite

Assuming you have python, pip and virtualenv, the `test.sh` script will run the test suite
against the configured (or default) target, and print the results to the STDOUT.

If there is no virtualenv installed in the current directory (in a directory named `.venv`),
test.sh will create one there and then install the required packages into it. Delete this
directory between test runs to be certain all the dependencies are up to date. Alternatively,
leave the virtualenv in place to minimise time and bandwidth of each test run. 

Typically, a developer making frequent changes would keep the virtualenv in place, but
integration tests would use a fresh install every time.


### Test runner options

test.sh inherits many features from the py.test package, run `test.sh --help` to see the
options.

Some output formatting options worth noting:
 * `test.sh -v` provides more verbose output
 * `test.sh --spec` produces verbose output in a diffent format
 * `test.sh --quite` supresses output unless a defect is found
 * `test.sh --junit-xml=path` produces test result in junit format, which may be useful
   for issue tracking through a CI server.


## Sample Code

`/util.py` contains code that may be useful if you are looking for a simple demonstration of ways to interact with a DNS NAPTR records.

For examples see `client_side/test_query_formation.py` or `/host_from_abn.py`. Note, the `./host_from_abn.sh` wrapper calls the python script with the appropraite virtualenv (same trick as `test.sh`), which may be a convenieint way to run it.
