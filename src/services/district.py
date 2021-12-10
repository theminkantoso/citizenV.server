from src.models.districtDb import DistrictDb
from src.models.cityProvinceDb import CityDb


class DistrictServices():

    # Tìm 1 quận/huyện trong 1 tỉnh theo tên
    @staticmethod
    def exist_district(Cname: str, Dname: str):
        c = CityDb.find_by_name(Cname)
        if c:
            CId = c.cityProvinceId
            d = DistrictDb.find_by_C_D_name(CId, Dname)
            if d:
                return d
            return 1  # district not exist
        return 2  # city not exist

    # Tìm bằng name (Tạm như này đã)
    @staticmethod
    def find_name(name):
        d = DistrictDb.find_by_name(name)
        if d:
            return d
        return None

    # Cấp mã cho 1 quận/huyện trong 1 tỉnh  ->cấp 2 số
    @staticmethod
    def create_district(data: dict):
        CId = data.get('cityProvinceId')
        c = CityDb.find_by_id(CId)
        if c:
            data["districtId"] = data["cityProvinceId"] * 100 + data["districtId"]
            Dname = data.get('districtName')
            if DistrictDb.find_by_C_D_name(CId, Dname):
                return 1  # tên quận/huyện đã có trong tỉnh/tp
            if DistrictDb.find_by_id(data["districtId"]):
                return 2  # id quận/huyện đã tồn tại
            d = DistrictDb(**data)
            try:
                d.save_to_db()
            except:
                return 3  # error save
            return 4  # added
        return 5  # city not exist

    # Xoá 1 quận/huyện trong 1 tỉnh/thành phố khỏi danh sách
    @staticmethod
    def delete_district(Cname, Dname):
        c = CityDb.find_by_name(Cname)
        if c:
            CId = c.cityProvinceId
            d = DistrictDb.find_by_C_D_name(CId, Dname)
            if d:
                d.delete_from_db()
                return 1  # deleted
            return 2  # district not exist
        return 3  # city not exist

    # Sửa thông tin 1 quận/huyện
    @staticmethod
    def update_district(d: DistrictDb, data: dict):
        CId = data["cityProvinceId"]
        if CityDb.find_by_id(CId):
            Dname = data["districtName"]
            DId = data["districtId"]  # Id update (đúng số lượng 2_4_6_8)
            find = DistrictDb.find_by_C_Dname(CId, Dname)
            if (DistrictDb.find_by_id(DId) and (d.districtId != DId)) \
                    or (((d.districtName != Dname) or (d.cityProvinceId != CId)) and (find and len(find) >= 1)):
                return 1  # can't update
            if CId != (DId - DId % 100)/100:
                return 0
            try:
                d.districtId = DId
                d.districtName = Dname
                d.cityProvinceId = CId
                d.created = data["created"]
                d.save_to_db()
            except:
                return 2  # error
            return d
        return 3  # city not exist

    # List quận/huyện
    @staticmethod
    def list_dictrict_in_city(name):
        c = CityDb.find_by_name(name)
        if c:
            id = c.cityProvinceId
            districts = DistrictDb.find_by_CityId(id)
            return districts
        return None