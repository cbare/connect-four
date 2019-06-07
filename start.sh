#!/bin/bash

CMND=$1
if [ -z $CMND ]; then CMND="flask"; fi

if [ $CMND = "flask" ]; then
    PYTHONPATH=`pwd`/src FLASK_APP=api.py flask run --host=0.0.0.0
fi

if [ $CMND = "test" ]; then
    PYTHONPATH=`pwd`/src py.test -v -Wignore::DeprecationWarning
fi
