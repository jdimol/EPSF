import json
from app import db, ma
# from dataclasses import dataclass, field
#
# import marshmallow_dataclass
# import marshmallow.validate


class Attributes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200))
    rrv = []
    kpi = db.Column(db.Boolean)
    pid = db.Column(db.Integer)
    weight = db.Column(db.Float)
    kpi_type = db.Column(db.String(80))
    high_better = db.Column(db.Boolean)
    value = None

    def __init__(self, i_d, name, kpi, pid, kpi_type, high_better, weight):
        self.id = i_d
        self.name = name
        self.kpi = kpi
        self.pid = pid
        self.kpi_type = kpi_type
        self.high_better = high_better
        self.weight = weight

    @classmethod
    def from_json(cls, json_string):
        if type(json_string) == type(str):
            json_dict = json.loads(json_string)
            return cls(**json_dict)
        else:
            return cls(**json_string)


class AttrSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'kpi', 'pid', 'kpi_type', 'weight', 'value', 'rsrv')


# Init schema
attr_schema = AttrSchema()
attrs_schema = AttrSchema(many=True)


#
# with open('attributes.json') as file:
#     # Hierarchical Structure Attributes
#     data = json.load(file)
