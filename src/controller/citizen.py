from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.core.auth import crud_permission_required, authorized_required
from flask_restful import Resource, reqparse
from src.services.citizen import CitizenServices
from src.services.group import GroupServices


class Citizen(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str)
    parser.add_argument("DOB", type=str)
    parser.add_argument("sex", type=str)
    parser.add_argument("maritalStatus", type=str)
    parser.add_argument("nation", type=str)
    parser.add_argument("religion", type=str)
    parser.add_argument("permanentResidence", type=str)
    parser.add_argument("temporaryResidence", type=str)
    parser.add_argument("educationalLevel", type=str)
    parser.add_argument("job", type=str)

    # Tìm kiếm 1 citizen
    @jwt_required()
    @authorized_required(roles=[1, 2, 3, 4])
    def get(self, citizen_id):
        id_acc = get_jwt_identity()
        # Kiểm tra citizen_id tồn tại hay không
        citizen = CitizenServices.exist_citizen(id_acc, citizen_id)
        if citizen == 0:
            return {'message': "Invalid id"}, 400
        elif citizen == 1:
            return {"message": "not authorized"}, 403
        elif citizen:
            return citizen.json(), 200
        return {'message': 'citizen not found.'}, 404

    # Xoá 1 citizen  khỏi danh sách
    @jwt_required()
    @authorized_required(roles=[4])  # B1
    @crud_permission_required
    def delete(self, citizen_id):
        id_acc = get_jwt_identity()
        # Kiểm tra citizen_id tồn tại không
        c = CitizenServices.exist_citizen(id_acc, citizen_id)
        if c == 0:
            return {'message': "Invalid cccd"}, 400
        elif c == 1:
            return {"message": "not authorized"}, 403
        elif c:
            # Nếu citizen_id tồn tại
            citizen = CitizenServices.delete_citizen(c)
            if citizen == 1:
                return {"message": "An error occurred deleting the citizen."}, 500
            if citizen == 2:
                return {'message': 'citizen deleted.'}, 200
        return {'message': 'citizen not found.'}, 404

    # Chỉnh sửa thông tin 1 citizen
    # Nhập liệu 1 citizen
    @jwt_required()
    @authorized_required(roles=[4])  # Sửa bởi B1
    @crud_permission_required
    def put(self, citizen_id):
        id_acc = get_jwt_identity()
        # Kiểm  tra citizenId hợp lệ không
        citi = CitizenServices.exist_citizen(id_acc, citizen_id)
        if citi == 0:
            return {'message': "Invalid id"}, 400
        elif citi == 1:
            return {"message": "not authorized"}, 403
        elif citi is None:
            return {'message': 'citizenId not found.'}, 404
        else:
            # Nếu citizenId tồn tại
            data = Citizen.parser.parse_args()
            # Kiểm tra hợp lệ giá trị đầu vào
            c = CitizenServices.validate(data)
            if c == 0:
                return {'message': "Invalid DOB"}, 400
            elif c == 1:
                return {'message': "Invalid sex"}, 400
            elif c == 2:
                return {'message': "Invalid marital status"}, 400
            elif c == 3:
                return {'message': "Invalid edu_level"}, 400
            else:
                # Nếu giá trị đầu vào hợp lệ
                citizen = CitizenServices.update_citizen(data, citi, id_acc)
                if citizen == 0:
                    return {"message": "not authorized"}, 403
                elif citizen == 1:
                    return {"message": "An error occurred inserting the citizen."}, 500
                else:
                    return {"Message": "cityProvince updated. "}, 200


class add_Citizen(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("CCCD", type=str)  # CCCD = citizenId
    parser.add_argument("name", type=str)
    parser.add_argument("DOB", type=str)
    parser.add_argument("sex", type=str)
    parser.add_argument("maritalStatus", type=str)
    parser.add_argument("nation", type=str)
    parser.add_argument("religion", type=str)
    parser.add_argument("permanentResidence", type=str)
    parser.add_argument("temporaryResidence", type=str)
    parser.add_argument("educationalLevel", type=str)
    parser.add_argument("job", type=str)
    parser.add_argument('CCCD', type=str)

    # Nhập liệu 1 citizen
    @jwt_required()
    @authorized_required(roles=[4, 5])  # Nhập bởi B1, B2
    @crud_permission_required
    def post(self, group_id):
        id_acc = get_jwt_identity()
        data = add_Citizen.parser.parse_args()
        # Kiểm tra group_id tồn tại không
        g = GroupServices.exist_group(id_acc, group_id)
        if g == 0:
            return {'message': "Invalid group_id"}, 400
        elif g == 1 or (id_acc != group_id and len(id_acc) == 8):
            return {'message': "not authorized"}
        elif g is None:
            return {'message': 'groupId not found.'}, 404
        else:
            # Nếu group_id tồn tại
            # print(data['CCCD'])
            # kiểm tra hợp lệ giá trị đầu vào
            if not CitizenServices.cccd(data["CCCD"]):
                return {'message': "Invalid CCCD"}, 400
            c = CitizenServices.validate(data)
            if c == 0:
                return {'message': "Invalid DOB"}, 400
            elif c == 1:
                return {'message': "Invalid sex"}, 400
            elif c == 2:
                return {'message': "Invalid marital status"}, 400
            elif c == 3:
                return {'message': "Invalid edu_level"}, 400
            else:
                # Nếu giá trị đầu vào hợp lệ
                citizen = CitizenServices.create_citizen(data, id_acc, group_id)
                if citizen == 0:
                    return {"message": "not authorized"}, 403
                elif citizen == 1:
                    return {"message": "CCCD is exist"}, 403
                elif citizen == 2:
                    return {"message": "An error occurred inserting the citzem."}, 500
                else:
                    return {"Message": "cityProvince added. "}, 200


class all_Citizen(Resource):

    @jwt_required()
    @authorized_required(roles=[1, 2, 3, 4])
    def get(self):
        id_acc = get_jwt_identity()
        citizens = CitizenServices.all_citizen(id_acc)
        return {'Citizens': list(map(lambda x: x.json(), citizens))}

    @jwt_required()
    @authorized_required(roles=[1, 2, 3, 4])
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("areas", action='append')
        acc = get_jwt()
        role = acc['role']
        data = parser.parse_args()
        citizens = CitizenServices.all_citizen_by_list_areas(role, data["areas"])
        if citizens == 1:
            return {'message': "Invalid id in list"}, 400
        return {'Citizens': list(map(lambda x: x.json(), citizens))}




