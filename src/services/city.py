from src.models.cityProvinceDb import CityDb


class CityServices():

    # Xem tên tỉnh/Thành phố tồn tại không
    @staticmethod
    def exist_city(name: str):
        c = CityDb.find_by_name(name)
        if c:
            return c
        return None

    # Tìm 1 tỉnh/Thành phố qua Id
    @staticmethod
    def find_city_by_id(id : int):
        c = CityDb.find_by_id(id)
        if c:
            return c
        return None

    # Cấp mã cho 1 tỉnh/thành phố  ->cấp 2 số
    @staticmethod
    def create_city(data: dict):
        name = data.get('cityProvinceName')
        id = data.get('cityProvinceId')
        #  Kiểm tra xem name và id có tồn tại hay không
        if CityDb.find_by_name(name) and CityDb.find_by_id(id):
            return 1  # name and id exist
        if CityDb.find_by_name(name):
            return 2  # name exist
        if CityDb.find_by_id(id):
            return 3  # id exist
        c = CityDb(**data)
        try:
            c.save_to_db()
        except:
            return 4  # don't save
        return 5  # saved

    # xoá tỉnh/thành phố
    @staticmethod
    def delete_city(c: CityDb):
        try:
            c.delete_from_db()
        except:
            return 1  # error
        return 2  # deleted

    # sửa 1 tỉnh/thành phố
    @staticmethod
    def update_city(c: CityDb, data: dict):
        name = data["cityProvinceName"]
        id = data["cityProvinceId"]
        if (CityDb.find_by_name(name) and (c.cityProvinceName != name))\
                or (CityDb.find_by_id(id) and (c.cityProvinceId != id)):
            return 0
        c.cityProvinceId = id
        c.cityProvinceName = name
        c.created = data["created"]
        try:
            c.save_to_db()
        except:
            return 1
        return c

    # list tỉnh/thành phố
    @staticmethod
    def list_city():
        cities = CityDb.query.all()
        return cities
