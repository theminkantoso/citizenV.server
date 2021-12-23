from flask_restful import Resource, reqparse
from src.services.ward import WardServices
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.core.auth import crud_permission_required, authorized_required


class Ward(Resource):

    # Tìm 1 xã/phường theo id
    @jwt_required()
    @authorized_required(roles=[3])  # A3
    def get(self, ward_id):
        id_acc = get_jwt_identity()
        # Kiểm tra ward_id có tồn tại và người dùng có quyền không
        ward = WardServices.exist_ward(id_acc, ward_id)
        if ward == 0:
            return {'message': "Invalid id"}, 400
        elif ward == 1:
            return {"message": "not authorized"}, 403
        elif ward is None:
            return {'message': 'ward not found.'}, 404
        return ward.json(), 200

    # Thêm mã cho 1 xã/phường
    @jwt_required()
    @authorized_required(roles=[3])  # A3
    @crud_permission_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("wardId", type=str)
        parser.add_argument("wardName", type=str)
        data = parser.parse_args()

        id_acc = get_jwt_identity()
        # create
        w = WardServices.create_ward(id_acc, data)
        if w == 0:
            return {'message': "Invalid ward_id"}, 400
        elif w == 1:
            return {'message': "An ward with name in district already exists."}, 400
        elif w == 2:
            return {'message': "An ward with id in district already exists."}, 400
        elif w == 3:
            return {"message": "An error occurred inserting the ward."}, 500
        elif w == 4:
            return {"message": "ward added. "}, 200

    # Xoá 1 xã/phường  khỏi danh sách
    @jwt_required()
    @authorized_required(roles=[3])  # A3
    @crud_permission_required
    def delete(self, ward_id):
        id_acc = get_jwt_identity()
        # Kiểm tra ward_id có tồn tại và người dùng có quyền không
        w = WardServices.exist_ward(id_acc, ward_id)
        if w == 0:
            return {'message': "Invalid id"}, 400
        elif w == 1:
            return {"message": "not authorized"}, 403
        elif w is None:
            return {'message': 'ward not found.'}, 404
        else:  # ward_id tồn tại và người dùng có quyền
            ward = WardServices.delete_ward(w)
            if ward == 1:
                return {'message': 'An error occurred delete the ward.'}, 500
            else:
                return {'message': 'Ward deleted.'}, 200

    # Sửa thông tin 1 xã/phường
    @jwt_required()
    @authorized_required(roles=[3])
    @crud_permission_required
    def put(self, ward_id):
        parser = reqparse.RequestParser()
        parser.add_argument("wardName", type=str)
        data = parser.parse_args()

        id_acc = get_jwt_identity()
        # Kiểm tra ward_id có tồn tại và người dùng có quyền không
        w = WardServices.exist_ward(id_acc, ward_id)
        if w == 0:
            return {'message': "Invalid id"}, 400
        elif w == 1:
            return {"message": "not authorized"}, 403
        elif w is None:
            return {'message': 'ward not found.'}, 404
        else:
            # ward_id tồn tại và người dùng có quyền sửa
            ward = WardServices.update_ward(id_acc, w, data)
            if ward == 0:
                return {"message": "not change"}, 400
            elif ward == 1:
                return {'message': "Name update already exists in other ward."}, 400
            elif ward == 2:
                return {"message": "An error occurred update the ward."}, 500
            else:
                return {'message': 'Ward updated.'}, 200


class WardCompleted(Resource):

    # Cập nhật tiến độ
    @jwt_required()
    @authorized_required(roles=[4])  # B1
    @crud_permission_required
    def put(self, ward_id):
        parser = reqparse.RequestParser()
        parser.add_argument("completed", type=bool)
        data = parser.parse_args()

        id_acc = get_jwt_identity()
        # Cập nhật tiến độ
        ward = WardServices.completed(id_acc, ward_id, data)
        if ward == 0:
            return {'message': "Invalid id"}, 400
        elif ward == 1:
            return {"message": "not authorized"}, 403
        elif ward == 2:
            return {"message": "Not change"}, 400
        elif ward == 3:
            return {'message': "An error occurred update the ward."}, 500
        elif ward == 4:
            return {'message': 'ward not found.'}, 404
        return {'message': 'Ward updated.'}, 200


# Thống kê các xã/phường
class Wards(Resource):

    # Tất cả xã/phường trong 1 quận/huyện
    @jwt_required()
    @authorized_required(roles=[3])  # A3
    def get(self):
        id_acc = get_jwt_identity()
        ward = WardServices.list_ward_in_district(id_acc)
        return {"Areas": list(map(lambda x: x.json(), ward))}, 200
