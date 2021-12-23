from src.models.residentialGroupDb import GroupDb
from src.models.accountDb import AccountDb
from src.models.citizenDb import CitizenDb
import re


# so sánh chuỗi với chuỗi regex
def validate_regex(input_string, regex):
    pattern = re.compile(regex)
    if pattern.fullmatch(input_string):
        return True
    return False


class GroupServices:

    # Tìm 1 thôn/bản/tdp trong 1 xã/phường
    @staticmethod
    def exist_group(id_acc: str, group_id: str):
        # Validate group_id (đầu vào có 8 số)
        regex_id = '^(0[1-9]|[1-9][0-9]){4}$'
        if not validate_regex(group_id, regex_id):
            return 0  # Invalid id
        if id_acc != group_id[0:6] and len(id_acc) == 6:
            return 1  # not authorized
        group = GroupDb.find_by_id(group_id)
        if group:
            return group
        return None  # group not exist

    #  Tổng số dân ở 1 thôn/bản/tdp
    @staticmethod
    def sum_citizen_in_group(group_id: str):
        sum_citizen = CitizenDb.sum_all_citizen_in_group(group_id)
        return sum_citizen

    # Cấp mã cho 1 thôn/bản/tdp trong 1 xã/phường -> cấp 2 số
    @staticmethod
    def create_group(id_acc: str, data: dict):
        group_id = data["groupId"]
        group_name = data["groupName"]

        # Validate group_id (đầu vào là 2 số)
        regex_id = '^(0[1-9]|[1-9][0-9])$'
        if not validate_regex(group_id, regex_id):
            return 0  # Invalid group_id

        # groupId lưu ở database là 4 số
        data["groupId"] = id_acc + group_id
        if GroupDb.find_by_ward_group_name(id_acc, group_name):
            return 1  # Tên thôn/bản/tdp đã có trong xã/phường
        if GroupDb.find_by_id(data["groupId"]):
            return 2  # Id đã được cấp cho thôn/bản/tdp khác
        g = GroupDb(groupId=data["groupId"], groupName=group_name, wardId=id_acc)
        try:
            g.save_to_db()
        except:
            return 3  # error save
        return 4  # added

    # Xoá 1 thôn/bản/tdp khỏi danh sách
    @staticmethod
    def delete_group(group: GroupDb):
        try:
            group.delete_from_db()
        except Exception as e:
            print(e)
            return 0  # err
        return 1  # deleted

    # Sửa thông tin 1 xã/phường
    @staticmethod
    def update_group(id_acc: str, group: GroupDb, data: dict):
        group_name = data["groupName"]
        if group_name == group.groupName:
            return 0  # not change
        elif GroupDb.find_by_ward_group_name(id_acc, group_name):
            return 1  # Name update already exists in other Group
        try:
            group.groupName = group_name
            group.save_to_db()
        except:
            return 2  # error
        return None  # updated

    # List thôn/bản/tdp
    @staticmethod
    def list_group_in_ward(ward_id):
        # validate
        regex_id = '^(0[1-9]|[1-9][0-9]){3}$'
        if not validate_regex(ward_id, regex_id):
            return 0  # Invalid ward_id
        groups = GroupDb.find_by_ward_id(ward_id)
        if groups:
            return groups
        return None

    @staticmethod
    def list_group_progress(id: str):
        return GroupDb.find_join_account(id)

    @staticmethod
    def list_group_progress_specific(id_account, id_group):
        return GroupDb.find_join_account_specific(id_account, id_group)

    def get_group_name(id):
        return str(GroupDb.find_group_name(id)[0])

    @staticmethod
    def check_exist(id):
        return int(GroupDb.check_exist(id)) > 0
