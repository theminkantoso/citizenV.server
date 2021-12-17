from src.models.residentialGroupDb import GroupDb
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
        if id_acc != group_id[0:6]:
            return 1  # not authorized
        group = GroupDb.find_by_id(group_id)
        if group:
            return group
        return None  # group not exist

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
        g = GroupDb(groupId=data["groupId"], groupName=group_name, wardId=id_acc, completed=None)
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
        except:
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

    # tich tiến độ
    @staticmethod
    def completed(id_acc: str, group_id: str, data: dict):
        # Validate group_id (đầu vào là 8 số)
        regex_id = '^(0[1-9]|[1-9][0-9]){4}$'
        if not validate_regex(group_id, regex_id):
            return 0  # Invalid group_id
        group = GroupDb.find_by_id(group_id)
        completed = data["completed"]
        if group:
            if id_acc != group_id:
                return 1  # not authorized
            elif completed == group.completed:
                return 2  # not change
            try:
                group.completed = completed
                group.save_to_db()
            except Exception as e:
                print(e)
                return 3  # error
            return None  # updated
        return 4  # GroupId not found



    # List thôn/bản/tdp
    @staticmethod
    def list_ward_in_group(ward_id):
        groups = GroupDb.find_by_ward_id(ward_id)
        return groups
