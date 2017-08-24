#!/bin/bash
# https://pypi.python.org/pypi/pytest-html/1.9.0
# https://pypi.python.org/pypi/pytest-bdd/2.17.0
# https://pypi.python.org/pypi/pytest-doc/0.0.1
# https://pypi.python.org/pypi/pytest-json/0.4.0
export PYTHONDONTWRITEBYTECODE='1'

export DJANGO_SETTINGS_MODULE="dcl_server.settings"
export DCL_SECRET_KEY="asdf"

export DCL_OIDC_AUDIENCES="809799"  # default one, if unknown JWT token is provided
export DCL_OIDC_ENDPOINT="http://127.0.0.1:7500"  # default one, if unknown JWT token is provided
export DCL_DRFOIDC_ENDPOINTS_CONF="simguard;http://127.0.0.1:7500;http://127.0.0.1:7500;809799"

# sqlite database
export DCL_DB_ENGINE="django.db.backends.sqlite3"
export DCL_DB_NAME="::memory::"

source .venv/bin/activate || true
cd src

# standard run without custom reports
# --cov=dcl_server --cov-report html
py.test $@ || exit 1
# add --spec  for nice output, which is already can be considered a report
cd ..

deactivate || true

exit 0
