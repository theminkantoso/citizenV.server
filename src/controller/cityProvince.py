from flask_restful import Resource, reqparse
from src.models.cityProvinceDb import CityDb

class City(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("cityProvinceId", type=int)
    parser.add_argument("cityProvinceName", type=str)
    parser.add_argument("created", type=bool)

    # Tìm 1 tỉnh/thành phố theo tên
    def get(self, name):
        c = CityDb.find_by_name(name)
        if c :
            return c.json()
        return {'message': 'cityProvince not found'}, 404


    # Thêm mã cho 1 tỉnh/thành phố
    def post(self):
        data = City.parser.parse_args()
        if CityDb.find_by_name(data.get('cityProvinceName')):
            return {'message': "An cityProvince with name '{}' already exists.".format(data.get('cityProvinceName'))}, 400
        c = CityDb(**data)
        try:
            c.save_to_db()
        except:
            return {"message": "An error occurred inserting the cityProvince."}, 500
        return {"Message": "cityProvince added. "}, 201

    # Xoá 1 tỉnh/thành phố khỏi danh sách
    def delete(self, name):
        c = CityDb.find_by_name(name)
        if c:
            c.delete_from_db()
            return {'message': 'cityProvince deleted.'}
        return {'message': 'cityProvince not found.'}, 404

    # Sửa thông tin 1 tỉnh/thành phố
    def put(self, name):
        data = City.parser.parse_args()
        c = CityDb.find_by_name(name)
        if c:
            c.cityProvinceId = data["cityProvinceId"]
            c.cityProvinceName = data["cityProvinceName"]
            c.created = data["created"]
            try:
                c.save_to_db()
            except:
                return {"message": "An error occurred inserting the cityProvince."}, 500
            return c.json()
        return {'message': 'cityProvince not found.'}, 404

# Thống kê các tỉnh/thành phố
class Cities(Resource):
    def get(self):
        return {'Cities': list(map(lambda x: x.json(), CityDb.query.all()))}


