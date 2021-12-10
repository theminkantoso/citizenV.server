from flask_restful import Resource, reqparse
from src.services.district import DistrictServices
from src.services.city import CityServices

class District(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("districtId", type=int)
    parser.add_argument("districtName", type=str)
    parser.add_argument("cityProvinceId", type=int)
    parser.add_argument("created", type=bool)

    # Tìm 1 quận/huyện trong 1 tỉnh theo tên
    def get(self, Cname, Dname):
            d = DistrictServices.exist_district(Cname, Dname)
            if d == 1:
                return {'message': 'district not found'}, 404
            elif d == 2:
                return {'message': 'city not found'}, 404
            else:
                return d.json()

    # Thêm mã cho 1 quận/huyện
    def post(self):
        data = District.parser.parse_args()
        d = DistrictServices.create_district(data)
        if d == 1:
            return {'message': "An District with name in city  already exists."}, 400
        elif d == 2:
            return {'message': "An District with id in city  already exists."}, 400
        elif d == 3:
            return {"message": "An error occurred inserting the district."}, 500
        elif d == 4:
            return {"Message": "district added. "}, 201
        else:
            return {'message': 'City not found'}, 404

    # Xoá 1 quận/huyện trong 1 tỉnh/thành phố khỏi danh sách
    def delete(self, Cname, Dname):
        d = DistrictServices.delete_district(Cname, Dname)
        if d == 1:
            return {'message': 'District deleted.'}
        elif d == 2:
            return {'message': 'district not found.'}, 404
        else:
            return {'message': 'city not found.'}, 404

    # Sửa thông tin 1 quận/huyện
    def put(self, Cname, Dname):
        data = District.parser.parse_args()
        c = CityServices.exist_city(Cname)
        if c:
            d = DistrictServices.exist_district(Cname, Dname)
            if d !=1 and d !=2 :
                dic = DistrictServices.update_district(d, data)
                if dic ==0:
                    return {"message": "DistrictId not belong to CityId" }, 401
                if dic == 1:
                    return {'message': "An District update already exists."}, 400
                if dic == 2:
                    return {"message": "An error occurred inserting the district."}, 500
                if dic == 3:
                    return {'message': 'cityProvince update not found.'}, 404
                return dic.json()
            return {'message': 'district not found.'}, 404
        return {'message': 'cityProvince not found.'}, 404

# Tất cả quận/huyện trong tỉnh/thành phố
class Districts(Resource):

    def get(self, name):
        d = DistrictServices.list_dictrict_in_city(name)
        if d :
            return {"Districts in '{}'".format(name): list(map(lambda x: x.json(), d))}
        return {'message': 'cityProvince not found.'}, 404

