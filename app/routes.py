from app import app, api, testing, pop_data_fields
from flask_restx import Resource    # Api, fields,
from flask import jsonify, request
from app.models import *
from app.ahp.methods import numeric_rsrv, attr_rsrv
import time
# import json


# @app.route('/')
# def index():
#     return 'Edge PoP Selection Framework'


# Test api
# @api.route('/test')
# class dataclass(Resource):
#     def get(self):
#         return "Api 'GET' works!"


@testing.route('/kpis')
class getKpis(Resource):
    @staticmethod
    def get():
        temp = Attributes.query.filter_by(kpi=True)
        result = attrs_schema.dump(temp, many=True)
        return result, 200


@testing.route('/pop_data')
class postData(Resource):
    @api.expect([pop_data_fields])
    def post(self):

        # measure execution time
        start_time = time.time()    # end_time next

        data = request.get_json()
        input_kpis = sorted(data, key=lambda x: x["id"], reverse=True)

        kpis = Attributes.query.filter_by(kpi=True)
        kpis = sorted(kpis, key=lambda x: x.id, reverse=True)

        # Update value field
        for k in input_kpis:
            this_object = Attributes.query.get(k["id"])
            kpis[kpis.index(this_object)].value = k["data"]

        length = len(input_kpis[0]["data"])
        rsrm = [list([1] * length) for j in range(length)]  # Array, initialize rsrm

        # ====== Testing Code ======
        for k in kpis:
            if k.value is None:     # Put specific data if there is not at all.
                k.value = [1, 1, 1]
            k.rsrv = numeric_rsrv(k.value,rsrm)
            # print(k.rsrv)
        # ==========================

        # result = attrs_schema.dump(kpis, many=True)

        attributes = Attributes.query.filter_by(kpi=False)
        scores = attr_rsrv(attributes, kpis)
        end_time = time.time()
        # result = attrs_schema.dump(scores, many=True)
        # print(scores[0].rsrv, end_time-start_time)

        execution_time = end_time-start_time
        ranking_vector = scores[0].rsrv

        result = json.dumps({'Ranking': ranking_vector, 'Exec Time': execution_time})

        return result, 200

    # @api.expect(attr_data)
    # def post(self):
    #     temp = api.payload
    #     result = attrs_schema.dump(temp, many=True)
    #     return result, 200


@app.route('/db/initialise', methods=['GET', 'POST'])
def update_db():

    # Validation for JSON content
    db_state = (Attributes.query.all() == [])  # Empty Database Attributes

    if db_state and request.is_json:
        # Parse the JSON into a Python dictionary
        attrs = request.get_json()  # List of database attributes
        for data in attrs:
            a = Attributes.from_json(data)
            db.session.add(a)
            db.session.commit()
        return ' DB Initialisation Done.', 200

    else:
        return jsonify(attrs_schema.dump(Attributes.query.all(), many=True)), 'Attributes Table is ' \
                                                                      'not Empty. Do you want to update DB?'


if __name__ == "__main__":
    app.run()
