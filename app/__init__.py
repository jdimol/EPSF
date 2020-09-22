from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restx import Api, fields  # Resource, marshal
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'selection_db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)
# Migrate
migrate = Migrate(app, db)

# api
api = Api(app, version='1.0', title="EPoP Selection Mechanism", description="EPSM's APIs testing using Swagger.")
# api.init_app(app)

testing = api.namespace('testing', description="Get EPSM's db elements")

# Create PoP data model for swagger
pop_data_fields = api.model('PoPData', {
    'id': fields.Integer,
    'name': fields.String,
    'data': fields.List(fields.Integer)
})

pop_data_list_fields = api.model('PoPDataList', {
    'pops_data': fields.List(fields.Nested(pop_data_fields)),
})

from app import routes, models

# app start

print('\n***** PoP Selection API *****')

# Validations
print('\n**********')
try:
    temp = (models.Attributes.query.all() == [])  # Empty Database
    if temp:
        print('Empty Attributes Table.\n**********\n')
    else:
        print('DB State OK.\n**********\n')

except:
    print('Init DB or Empty DB exception')
