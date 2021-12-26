from flask_restful import Resource, reqparse
from src.services.district import DistrictServices
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.core.auth import crud_permission_required, authorized_required


class District(Resource):

    # Tìm 1 quận/huyện trong 1 tỉnh theo id
    @jwt_required()
    @authorized_required(roles=[2])  # A2
    def get(self, dist_id):
        id_acc = get_jwt_identity()
        # Kiểm tra dist_id có tồn tại và người dùng có quyền không
        dist = DistrictServices.exist_district(id_acc, dist_id)
        if dist == 0:
            return {'msg': "Invalid id"}, 400
        elif dist == 1:
            return {"msg": "not authorized"}, 403
        elif dist is None:
            return {'msg': 'district not found.'}, 404
        return dist.json(), 200

    # Thêm mã cho 1 quận/huyện
    @jwt_required()
    @authorized_required(roles=[2])  # A2
    @crud_permission_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("districtId", type=str)
        parser.add_argument("districtName", type=str)
        data = parser.parse_args()

        id_acc = get_jwt_identity()
        # create
        d = DistrictServices.create_district(id_acc, data)
        if d == 0:
            return {'msg': "Invalid dist_id"}, 400
        elif d == 1:
            return {'msg': "An District with name in city  already exists."}, 400
        elif d == 2:
            return {'msg': "An District with id in city already exists."}, 400
        elif d == 3:
            return {"msg": "An error occurred inserting the district."}, 500
        elif d == 4:
            return {"msg": "district added. "}, 200

    # Xoá 1 quận/huyện trong 1 tỉnh/thành phố khỏi danh sách
    @jwt_required()
    @authorized_required(roles=[2])  # A2
    @crud_permission_required
    def delete(self, dist_id):
        id_acc = get_jwt_identity()
        # Kiểm tra dist_id có tồn tại và người dùng có quyền không
        d = DistrictServices.exist_district(id_acc, dist_id)
        if d == 0:
            return {'msg': "Invalid id"}, 400
        elif d == 1:
            return {"msg": "not authorized"}, 403
        elif d is None:
            return {'msg': 'district not found.'}, 404
        elif d: # Kiểm tra dist_id có tồn tại và người dùng có quyền không
            dist = DistrictServices.delete_district(d)
            if dist == 1:
                return {'msg': 'District deleted.'}, 200
            else:
                return {"msg": "An error occurred delete the district."}, 500

    # Sửa thông tin 1 quận/huyện
    @jwt_required()
    @authorized_required(roles=[2])  # A2
    @crud_permission_required
    def put(self, dist_id):
        parser = reqparse.RequestParser()
        parser.add_argument("districtName", type=str)
        data = parser.parse_args()

        id_acc = get_jwt_identity()
        # Kiểm tra dist_id có tồn tại và người dùng có quyền không
        d = DistrictServices.exist_district(id_acc, dist_id)
        if d == 0:
            return {'msg': "Invalid id"}, 400
        elif d == 1:
            return {"msg": "not authorized"}, 403
        elif d is None:
            return {'msg': 'district not found.'}, 404
        # dist_id tồn tại và người dùng có quyền sửa
        dist = DistrictServices.update_district(id_acc, d, data)
        if dist == 0:
            return {"msg": "Not change"}, 400
        elif dist == 1:
            return {"msg": "Name  already exists in other District."}, 400
        if dist == 2:
            return {"msg": "An error occurred update the district."}, 500
        return {'msg': 'cityProvince updated.'}, 200


class Districts(Resource):

    # Tất cả quận/huyện trong 1 tỉnh/thành phố
    @jwt_required()
    @authorized_required(roles=[2])  # A2
    def get(self):
        id_acc = get_jwt_identity()
        dists = DistrictServices.list_district_in_city(id_acc)
        return {"Areas": list(map(lambda x: x.json(), dists))}, 200


class all_Districts_in_area(Resource):

    # Tất cả quận/huyện trong 1 tỉnh/thành phố
    @jwt_required()
    @authorized_required(roles=[1, 2])  # A1, A2
    def get(self, city_id):
        id_acc = get_jwt_identity()
        if len(id_acc) == 1 or (len(id_acc) == 2 and id_acc == city_id):
            dists = DistrictServices.list_district_in_city(city_id)
            if dists == 0:
                return {'msg': "Invalid city_id"}, 400
            elif dists is None:
                return {'msg': 'dists not found in city.'}, 404
            return {"Areas": list(map(lambda x: x.json1(), dists))}, 200
        return {"msg": "not authorized"}, 403
