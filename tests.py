# from app import db
# from app.models import Attributes
# from app.ahp.methods import numeric_rsrv, attr_rsrv, test
#
# print(test())
#
#
# # pidAttr = Attributes.query.get(attr.pid)
# # pidAttrRsrv = attr_rsrv(pidAttr)
# # print(pidAttr.name, pidAttrRsrv)

import numpy as np

n = 5
X = [[0 for j in range(n)] for i in range(n)]

counter = 0
for i in range(n):
    for j in range(n):
        X[i][j] = i+1
        print(X[i][j])

print(X, counter)
