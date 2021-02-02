# Edge PoP Selection Framework

## Abstract

EPSF is designed to meet a set of user's requirements on selecting the appropriate PoP at the edge of the network for deploying a network slice. 
Based on the user's inputs and the advertised data from EPoPs, the two-stage selection procedure filters and ranks the candidate EPoPs in order to meet the user's requirements and enable the optimal resource provisioning from the provider's perspective. The ranking is based on the AHP. This is implemented, using python, as a flask rest API.

## Prerequisites

Clone the repository locally

```bash
git clone https://github.com/jdimol/EPSF.git
```

Create a python virtual environment

```bash
python3 -m venv ../path/to/venv
```

or using the "virtualenv" package:
```bash
virtualenv ../path/to/venv
```

Activate the venv and install dependancies:
```bash
source /path/to/venv/bin/activate
```
open the pop_selection folder:
```bash
pip install -r requirements.txt
```

## Run the flask API

Export the FLASK_APP environment variable. In the pop_selection folder:

```bash
export FLASK_APP=selection.py
```

### Initialise the database:

```bash
flask db init
flask db migrate
```

If you get an error "Please edit configuration/connection/logging settings in .../alembic.ini' before proceeding." try:

```bash
flask db upgrade
```

### Run the application:

```bash
flask run
```
Application is now running on localhost.

## Store Attributes in the database

A hierarchical structure with the corresponding attributes is located in the static folder in the attributes.json file

Store this structure as objects in the db via an api call:

```bash
curl -X POST "http://127.0.0.1:5000/db/initialise" -H "accept: application/json" -H "Content-Type: application/json" -d @./static/attributes.json
```
### Test the API

GET request for the KPIs of the structure

```bash
curl --location --request GET '127.0.0.1:5000/epsm_api/kpis'
```

Or using swagger-ui in the http://127.0.0.1:5000

## Authors

* **Giannis Dimolitsas**
