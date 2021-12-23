from src.models.cityProvinceDb import CityDb
from src.models.accountDb import AccountDb
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
        if CityDb.find_by_name(name) or CityDb.find_by_id(city_id):
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
    def list_city_db():
        cities = CityDb.find_all()
        return cities

    @staticmethod
    def list_city_progress():
        """
        list cities managed by an A1 account
        no need to validate since input of this function is generated by backend
        :return: query result
        """
        return CityDb.find_join_account()

    @staticmethod
    def list_city_progress_specific(id):
        """
        list a specific city managed by an A1 account
        no need to validate since input of this function is generated by backend
        :param id: A1 account
        :return: query result
        """
        return CityDb.find_join_account_specific(id)

    @staticmethod
    def count_completed_cities():
        """
        count total completed cities
        :return: query result
        """
        return CityDb.count_completed()

    @staticmethod
    def count_total_cities():
        """
        count total cities
        :return: query result
        """
        return CityDb.count_total()

    @staticmethod
    def get_city_name(id):
        return str(CityDb.find_city_name(id)[0])

    @staticmethod
    def check_exist(id):
        return int(CityDb.check_exist(id)) > 0
