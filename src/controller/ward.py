from flask_restful import Resource, reqparse
from src.services.ward import WardServices
from src.services.district import DistrictServices

class Ward(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("wardId", type=int)
    parser.add_argument("wardName", type=str)
    parser.add_argument("districtId", type=int)
    parser.add_argument("created", type=bool)

    # Tìm 1 xã/phường theo tên
    def get(self, Dname, Wname):
        w = WardServices.exist_ward(Dname, Wname)
        if w == 1:
            return {'message': 'ward not found'}, 404
        elif w == 2:
            return {'message': 'district not found'}, 404
        else:
            return w.json()

    # Thêm mã cho 1 xã/phường
    def post(self):
        data = Ward.parser.parse_args()
        w = WardServices.create_ward(data)
        if w == 1:
            return {'message': "An ward with name in district already exists."}, 400
        elif w == 2:
            return {'message': "An ward with id in district already exists."}, 400
        elif w == 3:
            return {"message": "An error occurred inserting the ward."}, 500
        elif w == 4:
            return {"Message": "ward added. "}, 201
        else:
            return {'message': 'District not found'}, 404


    # Xoá 1 xã/phường trong 1 quận/huyện khỏi danh sách
    def delete(self, Dname, Wname):
        w = WardServices.delete_ward(Dname, Wname)
        if w == 1:
            return {'message': 'Ward deleted.'}
        elif w == 2:
            return {'message': 'ward not found.'}, 404
        else:
            return {'message': 'district not found.'}, 404

    # Sửa thông tin 1 xã/phường
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
    def get(self, name):
        w = WardServices.list_ward_in_district(name)
        if w :
            return {"Wards in '{}'".format(name): list(map(lambda x: x.json(), w))}
        return {'message': 'district not found.'}, 404

