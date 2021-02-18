#!/bin/bash

db_ipaddr="http://127.0.0.1:8080/db/initialise"
header1="Accept: application/json"
header2="Content-Type: application/json"

attrs=@../static/attributes.json

function db_init {
    curl -X POST "${db_ipaddr}" -H "${header1}" -H "${header2}" -d ${attrs}
}

db_init
