from flask_restful import Resource, reqparse
from src.services.city import CityServices
from flask_jwt_extended import jwt_required
from src.core.auth import crud_permission_required, authorized_required


class City(Resource):

    # Tìm 1 tỉnh/thành phố
    @jwt_required()
    @authorized_required(roles=[1])  # tất cả A1 đều có quyền truy vấn
    def get(self, city_id):
        # Kiểm ta city_id tồn tại không
        city = CityServices.exist_city(city_id)
        if city == 0:
            return {'message': "Invalid city_id"}, 400
        if city:  # city_id tồn tại
            return city.json(), 200
        return {'message': 'cityProvince not found.'}, 404

    # Thêm mã cho 1 tỉnh/thành phố
    @jwt_required()
    @authorized_required(roles=[1])  # tất cả A1 đều có quyền cấp phát
    @crud_permission_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("cityProvinceId", type=str)
        parser.add_argument("cityProvinceName", type=str)

        data = parser.parse_args()
        # create
        c = CityServices.create_city(data)
        if c == 0:
            return {'message': "Invalid id"}, 400
        elif c == 1:
            return {"message": "cityProvinceName or cityProvinceId already exists."}, 400
        elif c == 2:
            return {"message": "An error occurred inserting the cityProvince."}, 500
        else:
            return {"message": "cityProvince added. "}, 200

    # Xoá 1 tỉnh/thành phố khỏi danh sách
    @jwt_required()
    @authorized_required(roles=[1])  # tất cả A1 đều có quyền
    @crud_permission_required
    def delete(self, city_id):
        # Kiểm tra city_id tồn tại không
        c = CityServices.exist_city(city_id)
        if c == 0:
            return {'message': "Invalid id"}, 400
        if c:  # city_id tồn tại
            city = CityServices.delete_city(c, city_id)
            if city == 1:
                return {"message": "An error occurred deleting the cityProvince."}, 500
            if city == 2:
                return {'message': 'cityProvince deleted.'}, 200
        return {'message': 'cityProvince not found.'}, 404

    # Sửa thông tin 1 tỉnh/thành phố
    @jwt_required()
    @authorized_required(roles=[1])  # tất cả A1 đều có quyền
    @crud_permission_required
    def put(self, city_id):
        parser = reqparse.RequestParser()
        parser.add_argument("cityProvinceName", type=str)
        data = parser.parse_args()

        # Kiểm tra city_id tồn tại không
        c = CityServices.exist_city(city_id)
        if c == 0:
            return {'message': "Invalid id"}, 400
        elif c is None:
            return {'message': 'cityProvince not found.'}, 404
        else:  # city_id tồn tại
            city = CityServices.update_city(c, data)
            if city == 0:
                return {"message": "Not change"}, 400
            elif city == 1:
                return {"message": "Name  already exists in other cityProvince."}, 400
            elif city == 2:
                return {"message": "An error occurred updating the cityProvince."}, 500
            return {'message': 'cityProvince updated.'}, 200


# Danh sách các tỉnh/thành phố
class Cities(Resource):
    @jwt_required()
    @authorized_required(roles=[1])  # tất cả A1 đều có quyền
    def get(self):
        cities = CityServices.list_city_db()
        return {'Areas': list(map(lambda x: x.json(), cities))}, 200
