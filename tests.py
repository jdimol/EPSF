from app import db
from app.models import Attributes
from app.ahp.methods import numeric_rsrv, attr_rsrv, test

print(test())


# pidAttr = Attributes.query.get(attr.pid)
# pidAttrRsrv = attr_rsrv(pidAttr)
# print(pidAttr.name, pidAttrRsrv)
