from flask_restful import Resource, reqparse
from src.services.group import GroupServices
from src.services.ward import WardServices

class Group(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("groupId", type=int)
    parser.add_argument("groupName", type=str)
    parser.add_argument("wardId", type=int)
    parser.add_argument("created", type=bool)

    # Tìm 1 thôn/bản/tdp theo tên
    def get(self, Wname, Gname):
        g = GroupServices.exist_group(Wname, Gname)
        if g == 1:
            return {'message': 'group not found'}, 404
        elif g == 2:
            return {'message': 'ward not found'}, 404
        else:
            return g.json()

    # Thêm mã cho 1 thôn/bản/tdp
    def post(self):
        data = Group.parser.parse_args()
        g = GroupServices.create_group(data)
        if g == 1:
            return {'message': "An group with name in ward already exists."}, 400
        elif g == 2:
            return {'message': "An group with id in ward already exists."}, 400
        elif g == 3:
            return {"message": "An error occurred inserting the group."}, 500
        elif g == 4:
            return {"Message": "group added. "}, 201
        else:
            return {'message': 'ward not found'}, 404

    # Xoá 1 thôn/bản/tdp trong 1 xã/phường khỏi danh sách
    def delete(self, Wname, Gname):
        g = GroupServices.delete_group(Wname, Gname)
        if g == 1:
            return {'message': 'Group deleted.'}
        elif g == 2:
            return {'message': 'Group not found.'}, 404
        else:
            return {'message': 'Ward not found.'}, 404

    # Sửa thông tin 1 thôn/bản/tdp
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
    def get(self, name):
        g = GroupServices.list_ward_in_group(name)
        if g:
            return {"Groups in '{}'".format(name): list(map(lambda x: x.json(), g))}
        return {'message': 'ward not found.'}, 404

