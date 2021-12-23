from src.models.wardDb import WardDb
from src.models.accountDb import AccountDb
import re


# so sánh chuỗi với chuỗi regex
def validate_regex(input_string, regex):
    pattern = re.compile(regex)
    if pattern.fullmatch(input_string):
        return True
    return False


class WardServices:

    # Tìm 1 phường/xã trong 1 quận/huyện
    @staticmethod
    def exist_ward(id_acc, ward_id: str):
        # Validate ward_id , đầu vào có 6 chữ số
        regex_id = '^(0[1-9]|[1-9][0-9]){3}$'
        if not validate_regex(ward_id, regex_id):
            return 0  # Invalid ward_id
        elif id_acc != ward_id[0:4]:
            return 1  # not authorized
        ward = WardDb.find_by_id(ward_id)
        if ward:
            return ward
        return None  # ward not exist

    # Cấp mã cho 1 xã/phường trong 1 huyện  -> cấp 2 số
    @staticmethod
    def create_ward(id_acc: str, data: dict):
        ward_id = data["wardId"]
        ward_name = data["wardName"]

        # Validate ward_id (đầu vào là 2 số)
        regex_id = '^(0[1-9]|[1-9][0-9])$'
        if not validate_regex(ward_id, regex_id):
            return 0  # Invalid ward_id

        # wardId lưu ở database là 6 số
        data["wardId"] = id_acc + ward_id
        if WardDb.find_by_dist_ward_name(id_acc, ward_name):
            return 1  # Tên xã/phường đã có trong quận/huyện
        if WardDb.find_by_id(data["wardId"]):
            return 2  # Id đã được cấp cho xã khác
        w = WardDb(wardId=data["wardId"], wardName=ward_name, districtId=id_acc, completed=None)
        try:
            w.save_to_db()
        except:
            return 3  # error save
        return 4  # added

    # Xoá 1 xã/phường khỏi danh sách
    @staticmethod
    def delete_ward(ward: WardDb):
        try:
            ward.delete_from_db()
        except:
            return 1  # err
        return 0  # deleted

    # Sửa thông tin 1 xã/phường
    @staticmethod
    def update_ward(id_acc: str, ward: WardDb, data: dict):
        ward_name = data["wardName"]

        if ward_name == ward.wardName:
            return 0  # not change
        elif WardDb.find_by_dist_ward_name(id_acc, ward_name):
            return 1  # Name update already exists in other ward
        try:
            ward.wardName = ward_name
            ward.save_to_db()
        except:
            return 2  # error
        return None  # updated

    # cập nhật tiến độ
    @staticmethod
    def completed(id_acc: str, ward_id: str, data: dict):
        # Validate group_id (đầu vào là 6 số)
        regex_id = '^(0[1-9]|[1-9][0-9]){3}$'
        if not validate_regex(ward_id, regex_id):
            return 0  # Invalid group_id
        ward = WardDb.find_by_id(ward_id)
        completed = data["completed"]
        if ward:
            if id_acc != ward_id:
                return 1  # not authorized
            elif completed == ward.completed:
                return 2  # not change
            try:
                ward.completed = completed
                ward.save_to_db()
            except:
                return 3  # error
            return None  # updated
        return 4  # wardId not found

    # List xã/phường
    @staticmethod
    def list_ward_in_district(dist_id: str):
        wards = WardDb.find_by_district_id(dist_id)
        return wards

    @staticmethod
    def list_ward_progress(id: str):
        """
        list wards managed by a specific district account
        no need to validate since input of this function is generated by backend
        :param id: account id
        :return: query result
        """
        return WardDb.find_join_account(id)

    @staticmethod
    def list_ward_progress_specific(id_acc, id_req):
        """
        list a specific ward managed by a specific district account
        no need to validate since input of this function is generated by backend
        :param id_acc: account id
        :param id_req: ward request id
        :return: query result
        """
        return WardDb.find_join_account_specific(id_acc, id_req)

    @staticmethod
    def count_completed_wards(id_district):
        """
        count total completed ward given a specific district
        :param id_district: id district
        :return: query result
        """
        return WardDb.count_completed(id_district)

    @staticmethod
    def count_total_wards(id_district):
        """
        count total ward given a specific district
        :param id_district: id district
        :return: query result
        """
        return WardDb.count_total(id_district)

    @staticmethod
    def get_ward_name(id):
        return str(WardDb.find_ward_name(id)[0])

    @staticmethod
    def check_exist(id):
        return int(WardDb.check_exist(id)) > 0
