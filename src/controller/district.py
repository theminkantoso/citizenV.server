from flask_restful import Resource, reqparse
from src.models.districtDb import DistrictDb
from src.models.cityProvinceDb import CityDb

class District(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("districtId", type=int)
    parser.add_argument("districtName", type=str)
    parser.add_argument("cityProvinceId", type=int)
    parser.add_argument("created", type=bool)

    # Tìm 1 quận/huyện trong 1 tỉnh theo tên
    def get(self, Cname, Dname):
        c= CityDb.find_by_name(Cname)
        if c :
            CId = c.cityProvinceId
            d = DistrictDb.find_by_C_D_name(CId, Dname)
            if d :
                return d.json()
            return {'message': 'district not found'}, 404
        return {'message': 'city not found'}, 404

    # Thêm mã cho 1 quận/huyện
    def post(self):
        data = District.parser.parse_args()
        CId = data.get('cityProvinceId')
        if CityDb.find_by_id(CId):
            Cname = CityDb.find_by_id(CId).cityProvinceName
            Dname = data.get('districtName')
            if DistrictDb.find_by_C_D_name(CId, Dname):
                return {'message': "An District with name '{}' in '{}' already exists.".format(Dname, Cname)}, 400
            d = DistrictDb(**data)
            try:
                d.save_to_db()
            except:
                return {"message": "An error occurred inserting the district."}, 500
            return {"Message": "district added. "}, 201
        return {'message': 'City not found'}, 404

    # Xoá 1 quận/huyện trong 1 tỉnh/thành phố khỏi danh sách
    def delete(self, Cname, Dname):
        c = CityDb.find_by_name(Cname)
        if c :
            CId = c.cityProvinceId
            d = DistrictDb.find_by_C_D_name(CId, Dname)
            if d:
                d.delete_from_db()
                return {'message': 'District deleted.'}
            return {'message': 'district not found.'}, 404
        return {'message': 'city not found.'}, 404
    # Sửa thông tin 1 quận/huyện
    def put(self, Cname, Dname):
        data = District.parser.parse_args()
        c = CityDb.find_by_name(Cname)
        if not c :
            return {'message': 'city not found.'}, 404
        CId = c.cityProvinceId
        d = DistrictDb.find_by_C_D_name(CId, Dname)
        if d:
            CId = data["cityProvinceId"]
            if CityDb.find_by_id(CId):
                Cname = CityDb.find_by_id(CId).cityProvinceName
                Dname = data["districtName"]
                if len(DistrictDb.find_by_C_Dname(CId, Dname)) > 1:
                    return {'message': "An District with name '{}' in '{}' already exists.".format(Dname, Cname)}, 400
                try:
                    d.districtId = data["districtId"]
                    d.districtName = data["districtName"]
                    d.cityProvinceId = data["cityProvinceId"]
                    d.created = data["created"]
                    d.save_to_db()
                except:
                    return {"message": "An error occurred inserting the district."}, 500
                return d.json()
            return {'message': 'cityProvince not found.'}, 404
        return {'message': 'district not found.'}, 404

# Thống kê các quận/huyện
class Districts(Resource):
    # Tất cả quận/huyện trong tỉnh/thành phố
    def get(self, name):
        c = CityDb.find_by_name(name)
        if c :
            id = c.cityProvinceId
            return {"Districts in '{}'".format(name): list(map(lambda x: x.json(), DistrictDb.find_by_CityId(id)))}
        return {'message': 'cityProvince not found.'}, 404

    # Tất cả quận/huyện
    # def get(self):
    #     return {'Districts': list(map(lambda x: x.json(), DistrictDb.query.all()))}

