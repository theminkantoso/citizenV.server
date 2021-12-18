from src.models.cityProvinceDb import CityDb
import re

# regex to validate Id
regex_id = '^(0[1-9]|[1-9][0-9])$'


def validate_regex(input_string, regex):
    """
        Validate input string based on a given regex
        :param input_string: string needs to check
        :param regex: regex pattern
        :return: True if satisfied
    """
    pattern = re.compile(regex)
    if pattern.fullmatch(input_string):
        return True
    return False


class CityServices():

    # Xem tên tỉnh/Thành phố tồn tại không
    @staticmethod
    def exist_city(id: str):
        # Validate
        if not validate_regex(id, regex_id):
            return 0  # Invalid id
        c = CityDb.find_by_id(id)
        if c:
            return c
        return None

    # Cấp mã cho 1 tỉnh/thành phố  ->cấp 2 số
    @staticmethod
    def create_city(data: dict):
        name = data.get('cityProvinceName')
        id = data.get('cityProvinceId')

        # Validate đảm bảo 2 ký tự
        if not validate_regex(id, regex_id):
            return 0  # Invalid id

        #  Kiểm tra xem name và id có tồn tại hay không
        if CityDb.find_by_name(name) or CityDb.find_by_id(id):
            return 1  # name or id exist
        c = CityDb(**data)
        try:
            c.save_to_db()
        except:
            return 2  # don't save
        return 3  # saved

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
        if (c.cityProvinceId == id) and (c.cityProvinceName == name) and (c.created == data['created']):
            return 0
        if (CityDb.find_by_name(name) and (c.cityProvinceName != name)) \
                or (CityDb.find_by_id(id) and (c.cityProvinceId != id)):
            return 1
        # Validate
        if not validate_regex(id, regex_id):
            return 2  # Invalid id

        c.cityProvinceId = id
        c.cityProvinceName = name
        c.created = data["created"]
        try:
            c.save_to_db()
        except:
            return 3
        return c

    # list tỉnh/thành phố
    @staticmethod
    def list_city():
        cities = CityDb.query.all()
        return cities

    @staticmethod
    def list_city_db():
        return CityDb.find_all()
