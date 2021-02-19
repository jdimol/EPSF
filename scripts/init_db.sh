#!/bin/bash

## Change Directory to 

db_file="../app/selection_db.sqlite"
migr_folder="../migrations/"

if test -f "$db_file"; then
    rm -rf ${db_file}
    rm -rf ${migr_folder}
fi


## Run virtual environment
cd ..
source venv/bin/activate

export FLASK_APP=selection.py

flask db init
flask db migrate
flask db upgrade

## Init db using the api
cd scripts
db_ipaddr="http://127.0.0.1:8080/db/initialise"
header1="Accept: application/json"
header2="Content-Type: application/json"

attrs=@../static/attributes.json

function db_init {
    curl -X POST "${db_ipaddr}" -H "${header1}" -H "${header2}" -d ${attrs}
}

db_init
