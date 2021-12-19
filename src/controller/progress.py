from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.core.auth import authorized_required
from src.services.progressService import ProgressServices
from src.services.accountService import AccountService


class Progress(Resource):

    @jwt_required()
    @authorized_required([1, 2, 3])
    def get(self):
        id_acc = get_jwt_identity()
        claims = get_jwt()
        role = claims["role"]
        id_acc_len = len(id_acc)
        if role == 1:
            location = ProgressServices.list_city_progress()
            count_complete = ProgressServices.count_completed_cities()
            count_total = ProgressServices.count_total_cities()
        elif id_acc_len == 2:
            location = ProgressServices.list_district_progress(id_acc)
            count_complete = ProgressServices.count_completed_districts(id_acc)
            count_total = ProgressServices.count_total_districts(id_acc)
        elif id_acc_len == 4:
            location = ProgressServices.list_ward_progress(id_acc)
            count_complete = ProgressServices.count_completed_wards(id_acc)
            count_total = ProgressServices.count_total_wards(id_acc)
        else:
            return {"message": "Something went wrong"}, 404
        if location:
            return {"progress": ProgressServices.convert_to_list_dict(location), "completed": count_complete,
                    "total": count_total}, 200
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
        if not AccountService.validate_input_id(id_request):
            return {"message": "bad request"}, 400

        if role == 1:
            location = ProgressServices.list_city_progress_specific(id_request)
            count_complete = ProgressServices.count_completed_districts(id_request)
            count_total = ProgressServices.count_total_districts(id_request)
            if location:
                return ProgressServices.convert_to_json_progress_specific(location, count_complete, count_total), 200
            else:
                return {"message": "No location like that or invalid input"}, 404
        elif id_acc_len == 2:
            location = ProgressServices.list_district_progress_specific(id_acc, id_request)
            count_complete = ProgressServices.count_completed_wards(id_request)
            count_total = ProgressServices.count_total_wards(id_request)
            if location:
                return ProgressServices.convert_to_json_progress_specific(location, count_complete, count_total), 200
            else:
                return {"message": "No location like that or invalid input"}, 404
        elif id_acc_len == 4:
            location = ProgressServices.list_ward_progress_specific(id_acc, id_request)
            return ProgressServices.convert_to_json_dict_progress(location)
        else:
            return {"message": "Something went wrong"}, 404

    @jwt_required()
    @authorized_required([1, 2, 3])
    def post(self, id):
        id_acc = get_jwt_identity()
        claims = get_jwt()
        role = claims["role"]
        id_acc_len = len(id_acc)
        id_request = id
        if not AccountService.validate_input_id(id_request):
            return {"message": "bad request"}, 400

        if role == 1:
            email = str()
        elif id_acc_len == 2:

        elif id_acc_len == 4:

        else:
            return {"message": "Something went wrong"}, 404

