from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.core.auth import crud_permission_required, authorized_required
from src.services.city import CityServices
from src.services.district import DistrictServices
from src.services.ward import WardServices
from src.models.accountDb import AccountDb


class Progress(Resource):

    @jwt_required()
    @authorized_required([1, 2, 3])
    def get(self):
        id_acc = get_jwt_identity()
        id_acc_len = len(id_acc)
        if id_acc_len == 2:
            location = CityServices.list_city_db()
        elif id_acc_len == 4:
            location = DistrictServices.list_district_managed(id_acc)
        elif id_acc_len == 6:
            location = WardServices.list_ward_managed(id_acc)
        else:
            location = None
            return {"message": "Something went wrong"}, 404

        return

