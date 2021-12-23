from src.services.citizen import CitizenServices
from src.services.city import CityServices
from src.services.district import DistrictServices
from src.services.ward import WardServices
from src.services.group import GroupServices


class StatisticsService():

    @staticmethod
    def population(id, role):
        if id == 'A1' and role == 1:
            return int(CitizenServices.get_population_entire())
        elif role == 2:
            return int(CitizenServices.get_population_city(id))
        elif role == 3:
            return int(CitizenServices.get_population_district(id))
        elif role == 4:
            return int(CitizenServices.get_population_ward(id))
        elif role == 5:
            return int(CitizenServices.get_population_group(id))

    @staticmethod
    def stat_sex(id, role):
        if id == 'A1' and role == 1:
            return CitizenServices.get_stats_sex_entire()
        elif role == 2:
            return CitizenServices.get_stats_sex_city(id)
        elif role == 3:
            return CitizenServices.get_stats_sex_district(id)
        elif role == 4:
            return CitizenServices.get_stats_sex_ward(id)
        elif role == 5:
            return CitizenServices.get_stats_sex_group(id)

    @staticmethod
    def stat_edu(id, role):
        if id == 'A1' and role == 1:
            return CitizenServices.get_stats_edu_entire()
        elif role == 2:
            return CitizenServices.get_stats_edu_city(id)
        elif role == 3:
            return CitizenServices.get_stats_edu_district(id)
        elif role == 4:
            return CitizenServices.get_stats_edu_ward(id)
        elif role == 5:
            return CitizenServices.get_stats_edu_district(id)

    @staticmethod
    def stat_marital(id, role):
        if id == 'A1' and role == 1:
            return CitizenServices.get_marital_status_entire()
        elif role == 2:
            return CitizenServices.get_marital_status_city(id)
        elif role == 3:
            return CitizenServices.get_marital_status_district(id)
        elif role == 4:
            return CitizenServices.get_marital_status_ward(id)
        elif role == 5:
            return CitizenServices.get_marital_status_group(id)

    @staticmethod
    def stat_group_age(id, role):
        if id == 'A1' and role == 1:
            return CitizenServices.get_group_age_entire()
        elif role == 2:
            return CitizenServices.get_group_age_city(id)
        elif role == 3:
            return CitizenServices.get_group_age_district(id)
        elif role == 4:
            return CitizenServices.get_group_age_ward(id)
        elif role == 5:
            return CitizenServices.get_group_age_group(id)

    @staticmethod
    def get_name(id, role):
        if role == 2:
            return CityServices.get_city_name(id)
        elif role == 3:
            return DistrictServices.get_district_name(id)
        elif role == 4:
            return WardServices.get_ward_name(id)
        elif role == 5:
            return GroupServices.get_group_name(id)

    @staticmethod
    def convert_to_dict_sex(arr):
        """
        Convert query result to dictionary
        :param arr: input result
        :return: dictionary form, later convert to JSON
        """
        dict_out = {"Nam": 0, "Nu": 0}
        for i in range(len(arr)):
            dict_out.update({arr[int(i)][0]: arr[int(i)][1]})
        return dict_out

    @staticmethod
    def convert_to_dict_edu(arr):
        """
        Convert query result to dictionary
        :param arr: input result
        :return: dictionary form, later convert to JSON
        """
        dict_out = {"0/10": 0, "1/10": 0, "2/10": 0, "3/10": 0, "4/10": 0, "5/10": 0, "6/10": 0, "7/10": 0, "8/10": 0,
                    "9/10": 0, "10/10": 0, "0/12": 0, "1/12": 0, "2/12": 0, "3/12": 0, "4/12": 0, "5/12": 0, "6/12": 0,
                    "7/12": 0, "8/12": 0, "9/12": 0, "10/12": 0, "11/12": 0, "12/12": 0}
        for i in range(len(arr)):
            dict_out.update({arr[int(i)][0]: arr[int(i)][1]})
        return dict_out

    @staticmethod
    def convert_to_dict_marital(arr):
        """
        Convert query result to dictionary
        :param arr: input result
        :return: dictionary form, later convert to JSON
        """
        dict_out = {"Chua ket hon": 0, "Da ket hon": 0, "Ly hon": 0}
        for i in range(len(arr)):
            dict_out.update({arr[int(i)][0]: arr[int(i)][1]})
        return dict_out

    @staticmethod
    def convert_to_dict_group_age(arr):
        """
        Convert query result to dictionary
        :param arr: input result
        :return: dictionary form, later convert to JSON
        """
        dict_out = {"under 18": int(arr[0][0]), "19-45": int(arr[0][1]), "46-65": int(arr[0][2]),
                    "66-80": int(arr[0][3]), "above 80": int(arr[0][4])}
        return dict_out

    @staticmethod
    def check_valid_request(id_acc, id_req):
        if len(id_req) <= len(id_acc):
            return False
        id_req_cut = id_req[0:len(id_acc)]
        if id_req_cut != id_acc:
            return False
        return True

    @staticmethod
    def check_valid_request_role(id_req, role):
        """
        Ensure A1, A2, A3 can access down to ward level, only B1 can access residentialGroup
        :param id_req: input request
        :param role: role of account
        :return: True if request is at residentialGroup level and role is B1
        """
        if len(id_req) == 8 and role != 4:
            return False
        return True

    @staticmethod
    def check_request_two_digit(id_req):
        """
        Ensure request is 2,4,6 or 8 digits
        :param id_req: input request
        :return: True if statisfy condition above
        """
        return len(id_req) % 2 == 0 and 8 >= len(id_req) >= 2

    @staticmethod
    def gen_index_request(id_req):
        req_len = len(id_req)
        if req_len == 2:
            return 2
        elif req_len == 4:
            return 3
        elif req_len == 6:
            return 4
        elif req_len == 8:
            return 5