#!/bin/bash
export PYTHONPATH="/code:${PYTHONPATH}"
cd /code/src
gunicorn dcl_server.wsgi:application --workers=4 -b 0.0.0.0:8080
