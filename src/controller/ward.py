from flask_restful import Resource, reqparse
from src.services.ward import WardServices
from src.services.district import DistrictServices
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.core.auth import crud_permission_required, authorized_required


class Ward(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("wardId", type=str)
    parser.add_argument("wardName", type=str)
    parser.add_argument("districtId", type=str)
    parser.add_argument("created", type=bool)

    # Tìm 1 xã/phường theo id
    def get(self, id):
        pass

    # Thêm mã cho 1 xã/phường
    @jwt_required()
    @authorized_required(roles=[3])
    @crud_permission_required
    def post(self):
        data = Ward.parser.parse_args()
        w = WardServices.create_ward(data)
        if w == 0:
            return {'message': "Invalid dist_id"}, 400
        elif w == 1:
            return {'message': "Invalid ward_id"}, 400
        elif w == 2:
            return {'message': "An ward with name in district already exists."}, 400
        elif w == 3:
            return {'message': "An ward with id in district already exists."}, 400
        elif w == 4:
            return {"message": "An error occurred inserting the ward."}, 500
        elif w == 5:
            return {"Message": "ward added. "}, 200
        else:
            return {'message': 'District not found'}, 404

    # Xoá 1 xã/phường  khỏi danh sách
    @jwt_required()
    @authorized_required(roles=[3])
    @crud_permission_required
    def delete(self, id):
        ward = WardServices.delete_ward(id)
        if ward == 0:
            return {'message': "Invalid id"}, 400
        elif ward == 1:
            return {'message': 'Ward deleted.'}, 200
        else:
            return {'message': 'ward not found.'}, 404

    # Sửa thông tin 1 xã/phường
    @jwt_required()
    @authorized_required(roles=[3])
    @crud_permission_required
    def put(self, Dname, Wname):
        data = Ward.parser.parse_args()
        d = DistrictServices.find_name(Dname)
        if d:
            w = WardServices.exist_ward(Dname, Wname)
            if w != 1 and w != 2:
                wa = WardServices.update_ward(w, data)
                if wa == 0:
                    return {"message": "WardId not belong to districtId"}, 401
                if wa == 1:
                    return {'message': "An ward update already exists."}, 400
                if wa == 2:
                    return {"message": "An error occurred inserting the ward."}, 500
                if wa == 3:
                    return {'message': 'District update not found.'}, 404
                return wa.json()
            return {'message': 'ward not found.'}, 404
        return {'message': 'district not found.'}, 404


# Thống kê các xã/phường
class Wards(Resource):

    # Tất cả xã/phường trong 1 quận/huyện
    @jwt_required()
    @authorized_required(roles=[3])
    def get(self, dist_id):
        ward = WardServices.list_ward_in_district(dist_id)
        if ward == 0:
            return {'message': "Invalid id"}, 400
        if ward:
            return {"Wards in '{}'".format(dist_id): list(map(lambda x: x.json(), ward))}
        return {'message': 'district not found.'}, 404
