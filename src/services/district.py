from src.models.districtDb import DistrictDb
from src.models.cityProvinceDb import CityDb
import re

# so sánh chuỗi với chuỗi regex
def validate_regex(input_string, regex):
    pattern = re.compile(regex)
    if pattern.fullmatch(input_string):
        return True
    return False


class DistrictServices():

    # Tìm 1 quận/huyện trong 1 tỉnh theo id
    @staticmethod
    def exist_district(id: str):
        # Validate
        regex_id = '^(0[1-9]|[1-9][0-9]){2}$'
        if not validate_regex(id, regex_id):
            return 0  # Invalid id
        dist = DistrictDb.find_by_id(id)
        if dist:
            return dist
        return None  # district not exist

    # Cấp mã cho 1 quận/huyện trong 1 tỉnh  -> cấp 2 số
    @staticmethod
    def create_district(data: dict):
        city_id = data.get('cityProvinceId')
        dist_id = data.get('districtId')
        dist_name = data.get('districtName')

        # Validate city_id vả dist_id (cả 2 đều có 2 số)
        regex_id = '^(0[1-9]|[1-9][0-9])$'
        if (not validate_regex(city_id, regex_id)) or (not validate_regex(dist_id, regex_id)):
            return 0  # Invalid city_id or dist_id

        city = CityDb.find_by_id(city_id)
        if city:
            data["districtId"] = city_id + dist_id
            if DistrictDb.find_by_city_dist_name(city_id, dist_name):
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
    def delete_district(id: str):
        # Validate
        regex_id = '^(0[1-9]|[1-9][0-9]){2}$'
        if not validate_regex(id, regex_id):
            return 0  # Invalid id
        dist = DistrictDb.find_by_id(id)
        if dist:
            dist.delete_from_db()
            return 1  # deleted
        return 2  # district not exist

    # Sửa thông tin 1 quận/huyện
    @staticmethod
    def update_district(d: DistrictDb, data: dict):
        city_id = data["cityProvinceId"]
        dist_id = data["districtId"]
        dist_name = data["districtName"]
        created = data["created"]
        if (dist_id == d.districtId) and (dist_name == d.districtName) \
                and (city_id == d.cityProvinceId) and (created == d.created):
            return 0
        if CityDb.find_by_id(city_id):
            Dname = data["districtName"]
            DId = data["districtId"]  # Id update (đúng số lượng 2_4_6_8)
            find = DistrictDb.find_by_C_Dname(city_id, Dname)
            if (DistrictDb.find_by_id(DId) and (d.districtId != DId)) \
                    or (((d.districtName != Dname) or (d.cityProvinceId != city_id)) and (find and len(find) >= 1)):
                return 1  # can't update
            if city_id != (DId - DId % 100) / 100:
                return 0
            try:
                d.districtId = DId
                d.districtName = Dname
                d.cityProvinceId = city_id
                d.created = data["created"]
                d.save_to_db()
            except:
                return 2  # error
            return d
        return 3  # city not exist

    # List quận/huyện
    @staticmethod
    def list_dictrict_in_city(city_id: str):
        regex_id = '^(0[1-9]|[1-9][0-9])$'
        if not validate_regex(city_id, regex_id):
            return 0  # Invalid city_id
        city = CityDb.find_by_id(city_id)
        if city:
            districts = DistrictDb.find_by_city_id(city_id)
            return districts
        return None
