from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.core.auth import crud_permission_required, authorized_required
from flask_restful import Resource, reqparse
from src.services.citizen import CitizenServices


class Citizen(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("citizenId", type=int)
    parser.add_argument("name", type=str)
    parser.add_argument("DOB", type=str)
    parser.add_argument("sex", type=str)
    parser.add_argument("maritalStatus", type=str)
    parser.add_argument("nation", type=str)
    parser.add_argument("religion", type=str)
    parser.add_argument("CMND", type=str)
    parser.add_argument("permanentResidence", type=str)
    parser.add_argument("temporaryResidence", type=str)
    parser.add_argument("educationalLevel", type=str)
    parser.add_argument("job", type=str)
    parser.add_argument("groupId", type=str)

    # Tìm kiếm 1 citizen
    def get(self, id):
        id_acc = '38010101'
        citizen = CitizenServices.exist_citizen(id, id_acc)
        if citizen == 0:
            return {'message': "Invalid id"}, 400
        elif citizen == 1:
            return {"message": "not authorized"}, 403
        elif citizen:
            return citizen.json()
        return {'message': 'citizen not found.'}, 404

    # Nhập liệu 1 citizen
    # @jwt_required()
    def post(self):
        # id_acc = get_jwt_identity()  # Là B1 hoặc B2
        # Giả sử người nhập liệu là B2
        id_acc = '38010101'

        data = Citizen.parser.parse_args()
        citizen = CitizenServices.create_citizen(data, id_acc)
        if citizen == 2:
            return {"message": "An error occurred inserting the cityProvince."}, 500
        elif citizen == 3:
            return {"Message": "cityProvince added. "}, 201

    # Xoá 1 citizen  khỏi danh sách
    def delete(self, id):
        id_acc = '38010101'
        c = CitizenServices.exist_citizen(id, id_acc)
        if c == 0:
            return {'message': "Invalid id"}, 400
        elif c == 1:
            return {"message": "not authorized"}, 403
        elif c:
            citizen = CitizenServices.delete_citizen(c)
            if citizen == 1:
                return {"message": "An error occurred deleting the citizen."}, 500
            if citizen == 2:
                return {'message': 'citizen deleted.'}, 200
        return {'message': 'citizen not found.'}, 404

    # Chỉnh sửa thông tin 1 citizen
    def put(self, id):
        pass


class all_Citizen(Resource):
    def get(self):
        id_acc = "38010103"
        cities = CitizenServices.all_citizen_by_acc(id_acc)
        return {'Citizens': list(map(lambda x: x.json(), cities))}

