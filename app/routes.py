''' Edge Cloud Selection - FAHP Based Application '''

# EndPoints Implementation File
# EPSM API (/epsm_api) interacts with the MESON components.

'''
Features:
 1) Hierarchical Structure Definition - DataBase Initialisation.
 2) Weight Assignments for Specific Attributes
 3) Ranking Mechanism:
     - Can handle data for KPIs in an ETSI_MEC descriptor format.
     - or format specified in the swagger.json file in "pop_data_fields"
       data structure.
'''

import time
import requests

from flask import jsonify, request
from flask_restx import Resource

from app import app, api, epsm_api
from app import pop_data_fields, weight_assignment
from app.models import *
from app.ahp.methods import numeric_rsrv, attr_rsrv



@epsm_api.route('/kpis')
class getKpis(Resource):
    @staticmethod
    def get():
        temp = Attributes.query.filter_by(kpi=True)
        result = attrs_schema.dump(temp, many=True)
        return result, 200


@epsm_api.route('/consumer_requirements')
class weightAssignment(Resource):
    @api.expect(weight_assignment)
    def post(self):

        dict_data = dict(request.get_json())

        # Extract pref_location from dictionary
        loc_required = dict_data["pref_location"]
        del dict_data["pref_location"]

        # Find the specified attributes
        # Iteration for update weight field in the db
        for key, value in dict_data.items():
            temp = Attributes.query.filter_by(name=key).first()
            temp.weight = float(value)
            # Normalize weight assignment
            if temp.name == 'Cost':
                temp2 = Attributes.query.filter_by(name='Slice_Performance').first()
                temp2.weight = 0.9 - float(value)
            db.session.commit()
            print("Attribute " + key + "weight assignment OK!")

        return "Consumer's requirements assigned", 200
        # Weight data parsed


@epsm_api.route('/pop_data')
class postData(Resource):
    @staticmethod
    def post():

        appd_list = request.get_json()
        # Create a list with values for each KPI

        rank_data = []
        # Define rank objects temp
        kpi_dict = appd_list[0]['appD']['PoPKPIs']
        for key, val in kpi_dict.items():
            print(key)
            temp = Attributes.query.filter_by(name=key).first()
            rank_obj_temp = {"id": int(temp.id), "name": key, "data": [int(val)]}
            rank_data.append(rank_obj_temp)
        appd_list_temp = appd_list # store appds
        appd_list.pop(0)

        for kpi_obj in rank_data:
            for prov in appd_list:
                kpi_obj['data'].append(prov['appD']['PoPKPIs'][kpi_obj['name']])

        r_data = json.dumps(rank_data)
        url = 'http://127.0.0.1:8080/epsm_api/pop_ranking'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        req = requests.post(url, data=r_data, headers=headers)

        if req.json==[]:
            return 'Problem in the ranking process!', 500

        ranking = json.loads(req.json())
        ranking_vector = ranking['Ranking']
        prov_index = ranking_vector.index(max(ranking_vector))
        result = json.dumps({'Ranking': ranking_vector, 'prov_idex': prov_index})
        result = appd_list_temp[prov_index]

        return result, 200


@epsm_api.route('/pop_ranking')
class popRanking(Resource):
    @api.expect([pop_data_fields])
    def post(self):

        data = request.get_json()
        input_kpis = sorted(data, key=lambda x: x["id"], reverse=True)

        kpis = Attributes.query.filter_by(kpi=True)
        kpis = sorted(kpis, key=lambda x: x.id, reverse=True)

        # Update value field
        for k in input_kpis:
            this_object = Attributes.query.get(k["id"])
            kpis[kpis.index(this_object)].value = k["data"]

        for k in kpis:
            # Check empty values
            if k.value is None:
                error_msg('None value for the KPI: ' +  k.name)
                print('ERROR!')
                print(error_msg)
                return error_msg, 500
            # Ranking Calcuations for KPIs
            k.rsrv = numeric_rsrv(k.value, k.high_better)

        # Ranking Calculations for Attributes
        attributes = Attributes.query.filter_by(kpi=False)
        scores = attr_rsrv(attributes, kpis)

        for attr in scores:
            if attr.name=='Ranking':
                ranking_vector = attr.rsrv

        #max_score=max(ranking_vector)
        #prov_index = ranking_vector.index(max_score)
        #result = json.dumps({'Ranking': ranking_vector, 'Best_Prov_index': prov_index})
        result = ranking_vector
        print(result)
        return json.dumps({'Ranking':result})


@app.route('/db/initialise', methods=['GET', 'POST'])
def init_db():
    '''
        Hierarchical Structure Initialisation
        input: a JSON file which contains the KPIs
        and attributes of the hierarchical srtucture.

    '''
    # Validation for JSON content and Empty Database (Attributes)
    db_state = (Attributes.query.all() == [])

    if db_state and request.is_json:
        # Parse the JSON into a Python dictionary
        attrs = request.get_json()  # List of database attributes
        for data in attrs:
            a = Attributes.from_json(data)
            db.session.add(a)
            db.session.commit()
        return ' DB Initialisation Done.', 200
    else:
        # return already stored attributes
        attrs = Attributes.query.all()
        attrs = jsonify(attrs_schema.dump(attrs, many=True))
        msg = 'Attributes table is not empty.'
        return attrs, msg

# @app.route('/')
# def index():
#     return 'Hello, World!'


# Test api
# @api.route('/test')
# class dataclass(Resource):
#     def get(self):
#         return "Api 'GET' works!"
