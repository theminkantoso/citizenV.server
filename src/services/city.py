from src.models.cityProvinceDb import CityDb
import re

# regex to validate Id: 2 số
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


class CityServices:

    # Xem tên tỉnh/Thành phố tồn tại không
    @staticmethod
    def exist_city(city_id: str):
        # Validate
        if not validate_regex(city_id, regex_id):
            return 0  # Invalid id
        c = CityDb.find_by_id(city_id)
        if c:
            return c
        return None

    # Cấp mã cho 1 tỉnh/thành phố  ->cấp 2 số
    @staticmethod
    def create_city(data: dict):
        name = data.get('cityProvinceName')
        city_id = data.get('cityProvinceId')

        # Validate city_id - Id chỉ có 2 số
        if not validate_regex(city_id, regex_id):
            return 0  # Invalid id

        #  Kiểm tra xem name và id có tồn tại hay không
        if CityDb.find_by_name(name) or CityDb.find_by_id(id):
            return 1  # name or id exist
        c = CityDb(cityProvinceId=city_id, cityProvinceName=name, completed=None)
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
        if name == c.cityProvinceName:
            return 0  # not change
        if CityDb.find_by_name(name) == c:  # Kiểm tra có tên trùng hay không
            return 1
        c.cityProvinceName = name
        try:
            c.save_to_db()
        except:
            return 2  # not save
        return 3  # updated

    # list tỉnh/thành phố
    @staticmethod
    def list_city():
        cities = CityDb.query.all()
        return cities
