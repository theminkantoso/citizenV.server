from src.models.wardDb import WardDb
from src.models.districtDb import DistrictDb


class WardServices():

    # Tìm 1 phường/xã trong 1 quận/huyện
    @staticmethod
    def exist_ward(Dname: str, Wname: str):
        d = DistrictDb.find_by_name(Dname)
        if d:
            DId = d.districtId
            w = WardDb.find_by_D_Wname(DId, Wname)
            if w:
                return w
            return 1  # ward not exist
        return 2  # district not exist

    # Tìm bằng name (Tạm như này đã)
    @staticmethod
    def find_name(name):
        w = WardDb.find_by_name(name)
        if w:
            return w
        return None

    # Cấp mã cho 1 xã/phường trong 1 huyện  ->cấp 2 số
    @staticmethod
    def create_ward(data: dict):
        DId = data.get('districtId')
        d = DistrictDb.find_by_id(DId)
        if d:
            data["wardId"] = data["districtId"] * 100 + data["wardId"]
            Wname = data.get('wardName')
            if WardDb.find_by_D_Wname(DId, Wname):
                return 1  # Tên xã/phường đã có trong quận/huyện
            if WardDb.find_by_id(data["wardId"]):
                return 2  # Id đã được cấp cho xã khác
            w = WardDb(**data)

            try:
                w.save_to_db()
            except:
                return 3  # error save
            return 4  # added
        return 5  # district not exist

    # Xoá 1 xã/phường khỏi danh sách
    @staticmethod
    def delete_ward(Dname, Wname):
        d = DistrictDb.find_by_name(Dname)
        if d:
            DId = d.districtId
            w = WardDb.find_by_D_Wname(DId, Wname)
            if w:
                w.delete_from_db()
                return 1  # deleted
            return 2  # ward not exist
        return 3  # district not exist

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
    def list_ward_in_district(name):
        d = DistrictDb.find_by_name(name)
        if d:
            id = d.districtId
            wards = WardDb.find_by_DistrictId(id)
            return wards
        return None
