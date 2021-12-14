from flask_restful import Resource, reqparse
from src.services.district import DistrictServices
from src.services.city import CityServices


class District(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("districtId", type=str)
    parser.add_argument("districtName", type=str)
    parser.add_argument("cityProvinceId", type=str)
    parser.add_argument("created", type=bool)

    # Tìm 1 quận/huyện trong 1 tỉnh theo id
    def get(self, id):
        pass

    # Thêm mã cho 1 quận/huyện
    def post(self):
        data = District.parser.parse_args()
        d = DistrictServices.create_district(data)
        if d == 0:
            return {'message': "Invalid id"}, 400
        elif d == 1:
            return {'message': "An District with name in city  already exists."}, 400
        elif d == 2:
            return {'message': "An District with id already exists."}, 400
        elif d == 3:
            return {"message": "An error occurred inserting the district."}, 500
        elif d == 4:
            return {"Message": "district added. "}, 200
        else:
            return {'message': 'City not found'}, 404

    # Xoá 1 quận/huyện trong 1 tỉnh/thành phố khỏi danh sách
    def delete(self, id):
        d = DistrictServices.delete_district(id)
        if d == 0:
            return {'message': "Invalid id"}, 400
        elif d == 1:
            return {'message': 'District deleted.'}, 200
        else:
            return {'message': 'district not found.'}, 404

    # Sửa thông tin 1 quận/huyện
    def put(self, id):
        data = District.parser.parse_args()
        d = DistrictServices.exist_district(id)
        if d == 0:
            return {'message': "Invalid id"}, 400
        if d:
            dist = DistrictServices.update_district(d, data)
            if dist == 0:
                return {"message": "DistrictId not belong to CityId"}, 401
            if dist == 1:
                return {'message': "An District update already exists."}, 400
            if dist == 2:
                return {"message": "An error occurred inserting the district."}, 500
            if dist == 3:
                return {'message': 'cityProvince update not found.'}, 404
            return dist.json()
        return {'message': 'district not found.'}, 404


# Tất cả quận/huyện trong tỉnh/thành phố
class Districts(Resource):

    def get(self, city_id):
        dist = DistrictServices.list_dictrict_in_city(city_id)
        if dist == 0:
            return {'message': "Invalid id"}, 400
        if dist:
            return {"Districts in '{}'".format(city_id): list(map(lambda x: x.json(), dist))}
        return {'message': 'cityProvince not found.'}, 404
