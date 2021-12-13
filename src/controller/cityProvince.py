from flask_restful import Resource, reqparse
from src.services.city import CityServices

class City(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("cityProvinceId", type=int)
    parser.add_argument("cityProvinceName", type=str)
    parser.add_argument("created", type=bool)

    # Tìm 1 tỉnh/thành phố theo tên
    def get(self, name):
        c = CityServices.exist_city(name)
        if c :
            return c.json()
        return {'message': 'cityProvince not found'}, 404


    # Thêm mã cho 1 tỉnh/thành phố
    def post(self):
        data = City.parser.parse_args()
        c = CityServices.create_city(data)
        if c == 1:
            return {"message": "cityProvinceName and cityProvinceId already exists."}, 400
        elif c == 2:
            return {"message": "cityProvinceName already exists."}, 400
        elif c == 3:
            return {"message": "cityProvinceId already exists."}, 400
        elif c == 4:
            return {"message": "An error occurred inserting the cityProvince."}, 500
        else:
            return {"Message": "cityProvince added. "}, 201

    # Xoá 1 tỉnh/thành phố khỏi danh sách
    def delete(self, name):
        c = CityServices.exist_city(name)
        if c:
            delt = CityServices.delete_city(c)
            if delt == 1:
                return {"message": "An error occurred deleting the cityProvince."}, 500
            if delt == 2:
                return {'message': 'cityProvince deleted.'}, 200
        return {'message': 'cityProvince not found.'}, 404

    # Sửa thông tin 1 tỉnh/thành phố
    def put(self, name):
        data = City.parser.parse_args()
        c = CityServices.exist_city(name)
        if c:
            c = CityServices.update_city(c, data)
            if c == 0:
                return {"message": "cityProvinceName or cityProvinceId already exists in other cityProvince."}, 400
            if c == 1:
                return {"message": "An error occurred updating the cityProvince."}, 500
            return c.json()
        return {'message': 'cityProvince not found.'}, 404


# Danh sách các tỉnh/thành phố
class Cities(Resource):
    def get(self):
        cities = CityServices.list_city()
        return {'Cities': list(map(lambda x: x.json(), cities))}


