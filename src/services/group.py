from src.models.wardDb import WardDb
from src.models.residentialGroupDb import GroupDb
import re


# so sánh chuỗi với chuỗi regex
def validate_regex(input_string, regex):
    pattern = re.compile(regex)
    if pattern.fullmatch(input_string):
        return True
    return False


class GroupServices():

    # Tìm 1 thôn/bản/tdp trong 1 xã/phường
    @staticmethod
    def exist_group(group_id: int):
        # Validate
        regex_id = '^(0[1-9]|[1-9][0-9]){4}$'
        if not validate_regex(group_id, regex_id):
            return 0  # Invalid id
        group = GroupDb.find_by_id(group_id)
        if group:
            return group
        return None  # group not exist

    # Cấp mã cho 1 thôn/bản/tdp trong 1 xã/phường -> cấp 2 số
    @staticmethod
    def create_group(data: dict):
        ward_id = data.get('wardId')
        group_id = data["groupId"]
        group_name = data["groupName"]

        # Validate ward_id (6 số)
        regex_id = '^(0[1-9]|[1-9][0-9]){3}$'
        if not validate_regex(ward_id, regex_id):
            return 0  # Invalid dist_id

        # Validate ward_id (đầu vào là 2 số)
        regex_id = '^(0[1-9]|[1-9][0-9])$'
        if not validate_regex(group_id, regex_id):
            return 1  # Invalid ward_id

        ward = WardDb.find_by_id(ward_id)
        if ward:
            data["groupId"] = ward_id + group_id
            if GroupDb.find_by_ward_group_name(ward_id, group_name):
                return 2  # Tên thôn/bản/tdp đã có trong xã/phường
            if GroupDb.find_by_id(data["groupId"]):
                return 3  # Id đã được cấp cho thôn/bản/tdp khác
            g = GroupDb(**data)

            try:
                g.save_to_db()
            except:
                return 4  # error save
            return 5  # added
        return 6  # ward not exist

    # Xoá 1 thôn/bản/tdp khỏi danh sách
    @staticmethod
    def delete_group(group_id: int):
        # Validate
        regex_id = '^(0[1-9]|[1-9][0-9]){4}$'
        if not validate_regex(group_id, regex_id):
            return 0  # Invalid id
        group = GroupDb.find_by_id(group_id)
        if group:
            group.delete_from_db()
            return 1  # deleted
        return 2  # group not exist

    # Sửa thông tin 1 xã/phường
    @staticmethod
    def update_group(g: GroupDb, data: dict):
        WId = data["wardId"]
        if WardDb.find_by_id(WId):
            Gname = data["groupName"]
            GId = data["groupId"]  # Id update (đúng số lượng 2_4_6_8)
            find = GroupDb.find_by_W_Gname(WId, Gname)
            if (GroupDb.find_by_id(GId) and (g.groupId != GId)) \
                    or (((g.groupName != Gname) or (g.wardId != WId)) and (find and len(find) >= 1)):
                return 1  # can't update
            if WId != (GId - GId % 100) / 100:
                return 0
            try:
                g.districtId = GId
                g.districtName = Gname
                g.cityProvinceId = WId
                g.created = data["created"]
                g.save_to_db()
            except:
                return 2  # error
            return g
        return 3  # ward not exist

    # List thôn/bản/tdp
    @staticmethod
    def list_ward_in_group(ward_id):
        regex_id = '^(0[1-9]|[1-9][0-9]){3}$'
        if not validate_regex(ward_id, regex_id):
            return 0  # Invalid dist_id
        ward = WardDb.find_by_id(ward_id)
        if ward:
            groups = GroupDb.find_by_ward_id(ward_id)
            return groups
        return None
