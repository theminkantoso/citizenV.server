from flask_restful import Resource, reqparse
from src.services.group import GroupServices
from src.services.ward import WardServices
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.core.auth import crud_permission_required, authorized_required


class Group(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("groupId", type=str)
    parser.add_argument("groupName", type=str)
    parser.add_argument("wardId", type=str)
    parser.add_argument("created", type=bool)

    # Tìm 1 thôn/bản/tdp theo id
    def get(self, id):
        pass

    # Thêm mã cho 1 thôn/bản/tdp
    @jwt_required()
    @authorized_required(roles=[4])
    @crud_permission_required
    def post(self):
        data = Group.parser.parse_args()
        g = GroupServices.create_group(data)
        if g == 0:
            return {'message': "Invalid ward_id"}, 400
        elif g == 1:
            return {'message': "Invalid group_id"}, 400
        elif g == 2:
            return {'message': "An group with name in ward already exists."}, 400
        elif g == 3:
            return {'message': "An group with id in ward already exists."}, 400
        elif g == 4:
            return {"message": "An error occurred inserting the group."}, 500
        elif g == 5:
            return {"Message": "group added. "}, 201
        else:
            return {'message': 'ward not found'}, 404

    # Xoá 1 thôn/bản/tdp trong 1 xã/phường khỏi danh sách
    @jwt_required()
    @authorized_required(roles=[4])
    @crud_permission_required
    def delete(self, id):
        group = GroupServices.delete_group(id)
        if group == 0:
            return {'message': "Invalid id"}, 400
        elif group == 1:
            return {'message': 'Group deleted.'}, 200
        else:
            return {'message': 'Group not found.'}, 404

    # Sửa thông tin 1 thôn/bản/tdp
    @jwt_required()
    @authorized_required(roles=[4])
    @crud_permission_required
    def put(self, Wname, Gname):
        data = Group.parser.parse_args()
        w = WardServices.find_name(Wname)
        if w:
            g = GroupServices.exist_group(Wname, Gname)
            if g != 1 and g != 2:
                gr = GroupServices.update_group(g, data)
                if gr == 0:
                    return {"message": "GroupId not belong to wardId"}, 401
                if gr == 1:
                    return {'message': "An group update already exists."}, 400
                if gr == 2:
                    return {"message": "An error occurred inserting the group."}, 500
                if gr == 3:
                    return {'message': 'Ward update not found.'}, 404
                return gr.json()
            return {'message': 'group not found.'}, 404
        return {'message': 'ward not found.'}, 404


# Thống kê các thôn/bản/tdp
class Groups(Resource):
    # Tất cả thôn/bản/tdp trong 1 xã/phường
    @jwt_required()
    @authorized_required(roles=[4])
    def get(self, ward_id):
        group = GroupServices.list_ward_in_group(ward_id)
        if group == 0:
            return {'message': "Invalid id"}, 400
        elif group:
            return {"Groups in '{}'".format(ward_id): list(map(lambda x: x.json(), group))}
        return {'message': 'ward not found.'}, 404
