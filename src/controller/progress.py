from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.core.auth import crud_permission_required, authorized_required
from src.services.city import CityServices
from src.services.district import DistrictServices
from src.services.ward import WardServices
from src.services.coreService import Services
from src.services.accountService import AccountService


def convert_to_list_dict(arr):
    """
    append arrays element to create a json output
    :param arr: input array
    :return: json dictionary type
    """
    list_out = []
    for i in range(len(arr)):
        list_out.append(Services.convert_to_json_dict(arr[i]))
    return list_out


class Progress(Resource):

    @jwt_required()
    @authorized_required([1, 2, 3])
    def get(self):
        id_acc = get_jwt_identity()
        claims = get_jwt()
        role = claims["role"]
        id_acc_len = len(id_acc)
        if role == 1:
            location = CityServices.list_city_progress()
        elif id_acc_len == 2:
            location = DistrictServices.list_district_progress(id_acc)
        elif id_acc_len == 4:
            location = WardServices.list_ward_progress(id_acc)
        else:
            return {"message": "Something went wrong"}, 404
        if location:
            return {"progress": convert_to_list_dict(location)}, 200
        return {}, 200


class ProgressSpecific(Resource):

    @jwt_required()
    @authorized_required([1, 2, 3])
    def get(self, id):
        id_acc = get_jwt_identity()
        claims = get_jwt()
        role = claims["role"]
        id_acc_len = len(id_acc)
        id_request = id
        if role == 1:
            location = CityServices.list_city_progress_specific(id_request)
            # count
            # count complete
        elif id_acc_len == 2:
            location = DistrictServices.list_district_progress_specific(id_acc, id_request)
        elif id_acc_len == 4:
            location = WardServices.list_ward_progress_specific(id_acc, id_request)
        else:
            return {"message": "Something went wrong"}, 404
        if location:
            return Services.convert_to_json_dict(location), 200
        return {"message": "No location like that or invalid input"}, 404
