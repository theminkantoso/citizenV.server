from src.models.wardDb import WardDb
from src.models.districtDb import DistrictDb
import re


# so sánh chuỗi với chuỗi regex
def validate_regex(input_string, regex):
    pattern = re.compile(regex)
    if pattern.fullmatch(input_string):
        return True
    return False


class WardServices():

    # Tìm 1 phường/xã trong 1 quận/huyện
    @staticmethod
    def exist_ward(ward_id: str):
        # Validate
        regex_id = '^(0[1-9]|[1-9][0-9]){3}$'
        if not validate_regex(ward_id, regex_id):
            return 0  # Invalid id
        ward = WardDb.find_by_id(ward_id)
        if ward:
            return ward
        return None  # ward not exist

    # Cấp mã cho 1 xã/phường trong 1 huyện  -> cấp 2 số
    @staticmethod
    def create_ward(data: dict):
        dist_id = data.get('districtId')
        ward_id = data["wardId"]
        ward_name = data["wardName"]

        # Validate dist_id (4 số)
        regex_id = '^(0[1-9]|[1-9][0-9]){2}$'
        if not validate_regex(dist_id, regex_id):
            return 0  # Invalid dist_id

        # Validate ward_id (đầu vào là 2 số)
        regex_id = '^(0[1-9]|[1-9][0-9])$'
        if not validate_regex(ward_id, regex_id):
            return 1  # Invalid ward_id

        dist = DistrictDb.find_by_id(dist_id)
        if dist:
            data["wardId"] = dist_id + ward_id
            if WardDb.find_by_dist_ward_name(dist_id, ward_name):
                return 2  # Tên xã/phường đã có trong quận/huyện
            if WardDb.find_by_id(data["wardId"]):
                return 3  # Id đã được cấp cho xã khác
            w = WardDb(**data)

            try:
                w.save_to_db()
            except:
                return 4  # error save
            return 5  # added
        return 6  # district not exist

    # Xoá 1 xã/phường khỏi danh sách
    @staticmethod
    def delete_ward(ward_id: str):
        # Validate
        regex_id = '^(0[1-9]|[1-9][0-9]){3}$'
        if not validate_regex(ward_id, regex_id):
            return 0  # Invalid id
        ward = WardDb.find_by_id(ward_id)
        if ward:
            ward.delete_from_db()
            return 1  # deleted
        return 2  # ward not exist

    # Sửa thông tin 1 xã/phường
    @staticmethod
    def update_ward(w: WardDb, data: dict):
        DId = data["districtId"]
        if DistrictDb.find_by_id(DId):
            Wname = data["wardName"]
            WId = data["wardId"]  # Id update (đúng số lượng 2_4_6_8)
            find = WardDb.find_by_D_Wname(DId, Wname)
            if (WardDb.find_by_id(WId) and (w.wardId != WId)) \
                    or (((w.wardName != Wname) or (w.districtId != DId)) and (find and len(find) >= 1)):
                return 1  # can't update
            if DId != (WId - WId % 100) / 100:
                return 0
            try:
                w.districtId = WId
                w.districtName = Wname
                w.cityProvinceId = DId
                w.created = data["created"]
                w.save_to_db()
            except:
                return 2  # error
            return w
        return 3  # district not exist

    # List xã/phường
    @staticmethod
    def list_ward_in_district(dist_id: str):
        regex_id = '^(0[1-9]|[1-9][0-9]){2}$'
        if not validate_regex(dist_id, regex_id):
            return 0  # Invalid dist_id
        dist = DistrictDb.find_by_id(dist_id)
        if dist:
            wards = WardDb.find_by_district_id(dist_id)
            return wards
        return None

    # list wards managed by a specific district account
    # no need to validate since input of this function is generated by backend
    @staticmethod
    def list_ward_progress(id: str):
        return WardDb.find_join_account(id)

    # list a specific ward managed by a specific district account
    # no need to validate since input of this function is generated by backend
    @staticmethod
    def list_ward_progress_specific(id_acc, id_req):
        return WardDb.find_join_account_specific(id_acc, id_req)
