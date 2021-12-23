from flask_restful import Resource, reqparse
from src.services.group import GroupServices
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.core.auth import crud_permission_required, authorized_required


class Group(Resource):

    # Tìm 1 thôn/bản/tdp theo id
    @jwt_required()
    @authorized_required(roles=[4])  # B1
    def get(self, group_id):
        id_acc = get_jwt_identity()
        # Kiểm tra group_id có tồn tại và người dùng có quyền không
        group = GroupServices.exist_group(id_acc, group_id)
        if group == 0:
            return {'message': "Invalid id"}, 400
        elif group == 1:
            return {"message": "not authorized"}, 403
        elif group is None:
            return {'message': 'group not found.'}, 404
        else:
            return group.json(), 200

    # Thêm mã cho 1 thôn/bản/tdp
    @jwt_required()
    @authorized_required(roles=[4])  # B1
    @crud_permission_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("groupId", type=str)
        parser.add_argument("groupName", type=str)
        data = parser.parse_args()

        id_acc = get_jwt_identity()
        # create
        g = GroupServices.create_group(id_acc, data)
        if g == 0:
            return {'message': "Invalid group_id"}, 400
        elif g == 1:
            return {'message': "An group with name in ward already exists."}, 400
        elif g == 2:
            return {'message': "An group with id in ward already exists."}, 400
        elif g == 3:
            return {"message": "An error occurred inserting the group."}, 500
        elif g == 4:
            return {"message": "group added. "}, 200

    # Xoá 1 thôn/bản/tdp trong 1 xã/phường khỏi danh sách
    @jwt_required()
    @authorized_required(roles=[4])  # B1
    @crud_permission_required
    def delete(self, group_id):
        id_acc = get_jwt_identity()
        # Kiểm tra group_id có tồn tại và người dùng có quyền không
        g = GroupServices.exist_group(id_acc, group_id)
        if g == 0:
            return {'message': "Invalid id"}, 400
        elif g == 1:
            return {"message": "not authorized"}, 403
        elif g is None:
            return {'message': 'group not found.'}, 404
        else:
            # Kiểm tra group_id có tồn tại và người dùng có quyền không
            group = GroupServices.delete_group(g)
            if group == 1:
                return {'message': 'Group deleted.'}, 200
            else:
                return {'message': "An error occurred delete the group."}, 500

    # Sửa thông tin 1 thôn/bản/tdp
    @jwt_required()
    @authorized_required(roles=[4])  # B1
    @crud_permission_required
    def put(self, group_id):
        parser = reqparse.RequestParser()
        parser.add_argument("groupName", type=str)
        data = parser.parse_args()

        id_acc = get_jwt_identity()
        # Kiểm tra group_id có tồn tại và người dùng có quyền không
        g = GroupServices.exist_group(id_acc, group_id)
        if g == 0:
            return {'message': "Invalid id"}, 400
        elif g == 1:
            return {"message": "not authorized"}, 403
        elif g is None:
            return {'message': 'group not found.'}, 404
        else:
            # group_id tồn tại và người dùng có quyền sửa
            group = GroupServices.update_group(id_acc, g, data)
            if group == 0:
                return {"message": "Not change"}, 400
            if group == 1:
                return {"message": "Name  already exists in other District."}, 400
            if group == 2:
                return {'message': "An error occurred update the group."}, 500
            return {'message': 'Group updated.'}, 200


# Thống kê các thôn/bản/tdp
class Groups(Resource):

    # Tất cả thôn/bản/tdp trong 1 xã/phường
    @jwt_required()
    @authorized_required(roles=[4])  # B1
    def get(self):
        id_acc = get_jwt_identity()
        groups = GroupServices.list_group_in_ward(id_acc)
        return {"Areas": list(map(lambda x: x.json(), groups))}, 200
