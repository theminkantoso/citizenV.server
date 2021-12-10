from src.models.wardDb import WardDb
from src.models.residentialGroupDb import GroupDb

class GroupServices():

    # Tìm 1 thôn/bản/tdp trong 1 xã/phường
    @staticmethod
    def exist_group(Wname: str, Gname: str):
        w = WardDb.find_by_name(Wname)
        if w:
            WId = w.wardId
            g = GroupDb.find_by_W_Gname(WId, Gname)
            if g:
                return g
            return 1  # group not exist
        return 2  # ward not exist

    # Cấp mã cho 1 thôn/bản/tdp trong 1 xã/phường -> cấp 2 số
    @staticmethod
    def create_group(data: dict):
        WId = data.get('wardId')
        w = WardDb.find_by_id(WId)
        if w:
            data["groupId"] = data["WardId"] * 100 + data["groupId"]
            Gname = data.get('groupName')
            if GroupDb.find_by_W_Gname(WId, Gname):
                return 1  # Tên thôn/bản/tdp đã có trong xã/phường
            if GroupDb.find_by_id(data["groupId"]):
                return 2  # Id đã được cấp cho thôn/bản/tdp khác
            g = GroupDb(**data)

            try:
                g.save_to_db()
            except:
                return 3  # error save
            return 4  # added
        return 5  # ward not exist

    # Xoá 1 thôn/bản/tdp khỏi danh sách
    @staticmethod
    def delete_group(Wname, Gname):
        w = WardDb.find_by_name(Wname)
        if w:
            WId = w.wardId
            g = GroupDb.find_by_W_Gname(WId, Gname)
            if g:
                g.delete_from_db()
                return 1  # deleted
            return 2  # group not exist
        return 3  # ward not exist

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
    def list_ward_in_group(name):
        w = WardDb.find_by_name(name)
        if w:
            id = w.wardId
            groups = GroupDb.find_by_WardId(id)
            return groups
        return None