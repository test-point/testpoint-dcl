#!/bin/bash

# make the virtualenv if it does not exist already
if [ ! -d '.venv' ]
then
    virtualenv .venv
    . .venv/bin/activate 
    pip install -r requirements.txt
fi

# if configured,  over-write the defaut target
if [ -f 'config.sh' ]
then
    . config.sh
fi

mkdir -p var/screenshots
rm -rf var/screenshots/*

. .venv/bin/activate
py.test  --splinter-screenshot-dir=var/screenshots/ --splinter-webdriver=phantomjs $@
# py.test  --splinter-screenshot-dir=var/screenshots/ --splinter-webdriver=firefox $@
deactivate
