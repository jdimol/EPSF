# AHP methods for EPoP Selection Mechanism

import numpy as np

from app.models import Attributes


# Find rsrv for each KPI
def numeric_rsrv(values, check):

    rsrm = []  # Array, initialize rsrm
    # print(check)
    if check:
        length = len(values)
        for i in range(length):
            temp_row = []   # each row of rsrm as a list
            for j in range(length):
                temp_row.append(values[i]/values[j])
            rsrm.append(temp_row)
    else:
        length = len(values)
        for i in range(length):
            temp_row = []  # each row of rsrm as a list
            for j in range(length):
                temp_row.append(values[j] / values[i])
            rsrm.append(temp_row)

    # sum rows of rsrm
    s_rows = []
    for row in rsrm:
        s_rows.append(sum(row))

    # sum entire rsrm
    s_rsrm = sum(s_rows)

    rsrv = []   # initialise rsrv
    for elem in s_rows:
        rsrv.append(elem/s_rsrm)

    return rsrv


def boolean_rsrv():
    return 'ok'


def un_set_rsrv():
    return 'ok'


# Ranking calculation
# At any level of the hierarchical structure
# Until Attribute's pid = 0!
def attr_rsrv(attrs, kpis):

    # calculation of the score for every attribute
    attributes = sorted(attrs, key=lambda x: x.id, reverse=True)

    # for every attribute calculate rsrv
    for attr in attributes:    # comment iteration for testing

        # find siblings
        siblings = []
        for k in kpis:
            if attr.id == k.pid:
                # print(k.rsrv)
                siblings.append(k)
        if not siblings:
            for k in attributes:
                if attr.id == k.pid:
                    siblings.append(k)

        # weight vector & rsrm for attribute
        rsrm = []
        w_vector = []
        for s in siblings:
            w_vector.append(s.weight)
            rsrm.append(s.rsrv)

        # create the numpy arrays
        temp_rsrm = np.array(rsrm)
        rsrm_final = temp_rsrm.transpose()
        w = np.array(w_vector)

        # find rsrv
        rsrv = rsrm_final.dot(w)    # numpy array multiplication
        attr.rsrv = rsrv.tolist()

    return attributes


# Hanlde zero (0) kpi values
# Numeric case
def handle_zero_numeric():
    """ Avoid zero division error """
    return 'relative_value'


# Testing
def test():

    all_attrs = Attributes.query.all()
    test_attrs = []
    test_kpis = []

    for a in all_attrs:
        if a.kpi:
            test_kpis.append(a)
        else:
            test_attrs.append(a)

    for k in test_kpis:
        #print(k.name)
        k.value = [1, 2, 3]
        #print(k.value)
        k.rsrv = numeric_rsrv(k.value)
        # print(k.name + '__VALUE:__' + str(k.value) + '__RSRV:__ ' + str(k.rsrv))

    #for k in test_kpis:
        #print(k.value)
    # testing numeric rsrv
    # test_rsrv = numeric_rsrv(attr.value)
    # print(test_rsrv)
    # find numeric rsrv for every kpi
    # attr.rsrv = numeric_rsrv([4, 8, 4])
    attrs = attr_rsrv(test_attrs, test_kpis)

    #for attr in test_attrs:
        #print(attr.name, attr.weight)
    return 'ok'
