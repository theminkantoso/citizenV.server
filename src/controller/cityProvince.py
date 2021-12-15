from flask_restful import Resource, reqparse
from src.services.city import CityServices
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.core.auth import crud_permission_required, authorized_required


class City(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("cityProvinceId", type=str)
    parser.add_argument("cityProvinceName", type=str)
    parser.add_argument("created", type=bool)

    # Tìm 1 tỉnh/thành phố
    def get(self, id):
        pass

    # Thêm mã cho 1 tỉnh/thành phố
    @jwt_required()
    @authorized_required(roles=[1])
    @crud_permission_required
    def post(self):
        data = City.parser.parse_args()
        c = CityServices.create_city(data)
        if c == 0:
            return {'message': "Invalid id"}, 400
        elif c == 1:
            return {"message": "cityProvinceName or cityProvinceId already exists."}, 400
        elif c == 2:
            return {"message": "An error occurred inserting the cityProvince."}, 500
        else:
            return {"Message": "cityProvince added. "}, 201

    # Xoá 1 tỉnh/thành phố khỏi danh sách
    @jwt_required()
    @authorized_required(roles=[1])
    @crud_permission_required
    def delete(self, id):
        c = CityServices.exist_city(id)
        if c == 0:
            return {'message': "Invalid id"}, 400
        if c:
            city = CityServices.delete_city(c)
            if city == 1:
                return {"message": "An error occurred deleting the cityProvince."}, 500
            if city == 2:
                return {'message': 'cityProvince deleted.'}, 200
        return {'message': 'cityProvince not found.'}, 404

    # Sửa thông tin 1 tỉnh/thành phố
    @jwt_required()
    @authorized_required(roles=[1])
    @crud_permission_required
    def put(self, id):
        data = City.parser.parse_args()
        c = CityServices.exist_city(id)
        if c == 0:
            return {'message': "Invalid id"}, 400
        if c:
            city = CityServices.update_city(c, data)
            if city == 0:
                return {"message": "Not change"}, 200
            if city == 1:
                return {"message": "cityProvinceName or cityProvinceId already exists in other cityProvince."}, 400
            if city == 2:
                return {'message': "Invalid id"}, 400
            if city == 3:
                return {"message": "An error occurred updating the cityProvince."}, 500
            return city.json()
        return {'message': 'cityProvince not found.'}, 404


# Danh sách các tỉnh/thành phố
class Cities(Resource):
    @jwt_required()
    @authorized_required(roles=[1])
    def get(self):
        cities = CityServices.list_city()
        return {'Cities': list(map(lambda x: x.json(), cities))}
