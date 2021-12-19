from src.models.districtDb import DistrictDb
from src.models.accountDb import AccountDb
import re


# so sánh chuỗi với chuỗi regex
def validate_regex(input_string, regex):
    pattern = re.compile(regex)
    if pattern.fullmatch(input_string):
        return True
    return False


class DistrictServices:

    # Tìm 1 quận/huyện trong 1 tỉnh theo id
    @staticmethod
    def exist_district(id_acc: str, dist_id: str):
        # Validate dist_id , đầu vào có 4 chữ số
        regex_id = '^(0[1-9]|[1-9][0-9]){2}$'
        if not validate_regex(dist_id, regex_id):
            return 0  # Invalid dist_id
        # Kiểm tra người dùng có quyền truy vấn không
        elif id_acc != dist_id[0:2]:
            return 1  # not authorized
        dist = DistrictDb.find_by_id(dist_id)
        if dist:
            return dist
        return None  # district not exist

    # Cấp mã cho 1 quận/huyện trong 1 tỉnh  -> cấp 2 số
    @staticmethod
    def create_district(id_acc: str, data: dict):
        dist_id = data.get('districtId')
        dist_name = data.get('districtName')

        # Validate dist_id (đầu vào có 2 số)
        regex_id = '^(0[1-9]|[1-9][0-9])$'
        if not validate_regex(dist_id, regex_id):
            return 0  # Invalid dist_id

        # districtId lưu ở database là 4 số
        data["districtId"] = id_acc + dist_id
        if DistrictDb.find_by_city_dist_name(id_acc, dist_name):
            return 1  # tên quận/huyện đã có trong tỉnh/tp
        if DistrictDb.find_by_id(data["districtId"]):
            return 2  # id quận/huyện đã tồn tại
        d = DistrictDb(districtId=data["districtId"], districtName=dist_name, cityProvinceId=id_acc, completed=None)
        try:
            d.save_to_db()
        except Exception as e:
            print(e)
            return 3  # error save
        return 4  # added

    # Xoá 1 quận/huyện trong 1 tỉnh/thành phố khỏi danh sách
    @staticmethod
    def delete_district(dist: DistrictDb, dist_id: str):
        try:
            dist.delete_from_db()
            AccountDb.delete_account_by_delete_area(dist_id)
        except:
            return 0  # err
        return 1  # deleted

    # Sửa thông tin 1 quận/huyện
    @staticmethod
    def update_district(id_acc: str, dist: DistrictDb, data: dict):
        dist_name = data["districtName"]
        if dist_name == dist.districtName:
            return 0  # not change
        elif DistrictDb.find_by_city_dist_name(id_acc, dist_name):
            return 1  # Name update already exists in other District
        try:
            dist.districtName = dist_name
            dist.save_to_db()
        except Exception as e:
            print(e)
            return 2  # error
        return None  # updated

    # List quận/huyện
    @staticmethod
    def list_district_in_city(city_id: str):
        districts = DistrictDb.find_by_city_id(city_id)
        return districts
