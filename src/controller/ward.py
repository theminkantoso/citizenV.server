from flask_restful import Resource, reqparse
from src.models.districtDb import DistrictDb
from src.models.wardDb import WardDb

class Ward(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("wardId", type=int)
    parser.add_argument("wardName", type=str)
    parser.add_argument("districtId", type=int)
    parser.add_argument("created", type=bool)

    # Tìm 1 xã/phường theo tên
    def get(self, Dname, Wname):
        d = DistrictDb.find_by_name(Dname)
        if d:
            DId = d.districtId
            w = WardDb.find_by_D_Wname(DId, Wname)
            if w:
                return w.json()
            return {'message': 'Ward not found'}, 404
        return {'message': 'District not found'}, 404

    # Thêm mã cho 1 xã/phường
    def post(self):
        data = Ward.parser.parse_args()
        DId = data.get('districtId')
        if DistrictDb.find_by_id(DId):
            Dname = DistrictDb.find_by_id(DId).districtName
            Wname = data.get('wardName')
            if WardDb.find_by_D_Wname(DId, Wname):
                return {'message': "An Ward with name '{}' in '{}' already exists.".format(Wname, Dname)}, 400
            w = WardDb(**data)
            try:
                w.save_to_db()
            except:
                return {"message": "An error occurred inserting the ward."}, 500
            return {"Message": "ward added. "}, 201
        return {'message': 'District not found'}, 404

    # Xoá 1 xã/phường trong 1 quận/huyện khỏi danh sách
    def delete(self, Dname, Wname):
        d = DistrictDb.find_by_name(Dname)
        if d:
            DId = d.districtId
            w = WardDb.find_by_D_Wname(DId, Wname)
            if w:
                w.delete_from_db()
                return {'message': 'ward deleted.'}
            return {'message': 'ward not found.'}, 404
        return {'message': 'District not found.'}, 404

    # Sửa thông tin 1 xã/phường
    def put(self, Dname, Wname):
        data = Ward.parser.parse_args()
        d = DistrictDb.find_by_name(Dname)
        if not d:
            return {'message': 'District not found.'}, 404
        DId = d.districtId
        w = WardDb.find_by_D_Wname(DId, Wname)
        if w:
            DId = data["districtId"]
            if DistrictDb.find_by_id(DId):
                Dname = DistrictDb.find_by_id(DId).districtName
                Wname = data["wardName"]
                if len(WardDb.find_by_DWname(DId, Wname)) > 1:
                    return {'message': "An ward with name '{}' in '{}' already exists.".format(Wname, Dname)}, 400
                try:
                    w.wardId = data["wardId"]
                    w.wardName = data["wardName"]
                    w.districtId = data["districtId"]
                    w.created = data["created"]
                    w.save_to_db()
                except:
                    return {"message": "An error occurred inserting the ward."}, 500
                return w.json()
            return {'message': 'district not found.'}, 404
        return {'message': 'ward not found.'}, 404


# Thống kê các xã/phường
class Wards(Resource):
    # Tất cả xã/phường trong 1 quận/huyện
    def get(self, name):
        d = DistrictDb.find_by_name(name)
        if d :
            id = d.districtId
            return {"Wards in '{}'".format(name): list(map(lambda x: x.json(), WardDb.find_by_DistrictId(id)))}
        return {'message': 'district not found.'}, 404

    # Tất cả quận/huyện
    # def get(self):
    #     return {'Districts': list(map(lambda x: x.json(), DistrictDb.query.all()))}

