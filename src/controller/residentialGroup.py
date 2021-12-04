from flask_restful import Resource, reqparse
from src.models.residentialGroupDb import GroupDb
from src.models.wardDb import WardDb

class Group(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("groupId", type=int)
    parser.add_argument("groupName", type=str)
    parser.add_argument("wardId", type=int)
    parser.add_argument("created", type=bool)

    # Tìm 1 thôn/bản/tdp theo tên
    def get(self, Wname, Gname):
        w = WardDb.find_by_name(Wname)
        if w:
            WId = w.wardId
            g = GroupDb.find_by_W_Gname(WId, Gname)
            if g:
                return g.json()
            return {'message': 'Group not found'}, 404
        return {'message': 'Ward not found'}, 404

    # Thêm mã cho 1 thôn/bản/tdp
    def post(self):
        data = Group.parser.parse_args()
        WId = data.get('wardId')
        if WardDb.find_by_id(WId):
            Wname = WardDb.find_by_id(WId).wardName
            Gname = data.get('groupName')
            if GroupDb.find_by_W_Gname(WId, Gname):
                return {'message': "An Group with name '{}' in '{}' already exists.".format(Gname, Wname)}, 400
            g = GroupDb(**data)
            try:
                g.save_to_db()
            except:
                return {"message": "An error occurred inserting the group."}, 500
            return {"Message": "group added. "}, 201
        return {'message': 'Ward not found'}, 404

    # Xoá 1 thôn/bản/tdp trong 1 xã/phường khỏi danh sách
    def delete(self, Wname, Gname):
        w = WardDb.find_by_name(Wname)
        if w:
            WId = w.wardId
            g = GroupDb.find_by_W_Gname(WId, Gname)
            if g:
                g.delete_from_db()
                return {'message': 'group deleted.'}
            return {'message': 'group not found.'}, 404
        return {'message': 'Ward not found.'}, 404

    # Sửa thông tin 1 thôn/bản/tdp
    def put(self, Wname, Gname):
        data = Group.parser.parse_args()
        w = WardDb.find_by_name(Wname)
        if not w:
            return {'message': 'Ward not found.'}, 404
        WId = WardDb.find_by_name(Wname).wardId
        g = GroupDb.find_by_W_Gname(WId, Gname)
        if g:
            WId = data["wardId"]
            if WardDb.find_by_id(WId):
                Wname = WardDb.find_by_id(WId).wardName
                Gname = data["groupName"]
                if len(GroupDb.find_by_WGname(WId, Gname)) > 1:
                    return {'message': "An group with name '{}' in '{}' already exists.".format(Gname, Wname)}, 400
                try:
                    g.groupId = data["groupId"]
                    g.groupName = data["groupName"]
                    g.wardId = data["wardId"]
                    g.created = data["created"]
                    g.save_to_db()
                except:
                    return {"message": "An error occurred inserting the group."}, 500
                return g.json()
            return {'message': 'ward not found.'}, 404
        return {'message': 'group not found.'}, 404


# Thống kê các thôn/bản/tdp
class Groups(Resource):
    # Tất cả thôn/bản/tdp trong 1 xã/phường
    def get(self, name):
        w = WardDb.find_by_name(name)
        if w :
            id = w.wardId
            return {"Groups in '{}'".format(name): list(map(lambda x: x.json(), GroupDb.find_by_WardId(id)))}
        return {'message': 'ward not found.'}, 404

    # Tất cả quận/huyện
    # def get(self):
    #     return {'Districts': list(map(lambda x: x.json(), DistrictDb.query.all()))}

