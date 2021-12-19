from src.services.city import CityServices
from src.services.district import DistrictServices
from src.services.ward import WardServices


class ProgressServices():
    @staticmethod
    def convert_to_json_dict_progress(arr):
        """
        create dictionary type of array elements
        :param arr: array in
        :return: dictionary format
        """
        complete = arr[2]
        end_time = arr[3]
        if complete is None:
            complete = ""
        if end_time is None:
            end_time = ""
        return {
            "id": arr[0],
            "name": arr[1],
            "completed": complete,
            "endTime": end_time
        }

    @staticmethod
    def convert_to_json_progress_specific(arr, count_completed, count_total):
        """
        create dictionary type of array elements and values
        :param arr: input array
        :param count_completed: input int
        :param count_total: input int
        :return: dictionary format
        """
        complete = arr[2]
        end_time = arr[3]
        if complete is None:
            complete = ""
        if end_time is None:
            end_time = ""
        return {
            "id": arr[0],
            "name": arr[1],
            "completed": complete,
            "endTime": end_time,
            "countCompleted": count_completed,
            "total": count_total
        }

    @staticmethod
    def convert_to_list_dict(arr):
        """
        append arrays element to create a json output
        :param arr: input array
        :return: json dictionary type
        """
        list_out = []
        for i in range(len(arr)):
            list_out.append(ProgressServices.convert_to_json_dict_progress(arr[i]))
        return list_out

    @staticmethod
    def count_completed_cities():
        return int(CityServices.count_completed_cities())

    @staticmethod
    def count_total_cities():
        return int(CityServices.count_total_cities())

    @staticmethod
    def count_completed_districts(id_acc):
        return int(DistrictServices.count_completed_districts(id_acc))

    @staticmethod
    def count_total_districts(id_acc):
        return int(DistrictServices.count_total_districts(id_acc))

    @staticmethod
    def count_completed_wards(id_acc):
        return int(WardServices.count_completed_wards(id_acc))

    @staticmethod
    def count_total_wards(id_acc):
        return int(WardServices.count_total_wards(id_acc))

    @staticmethod
    def list_city_progress():
        return CityServices.list_city_progress()

    @staticmethod
    def list_city_progress_specific(id_request):
        return CityServices.list_city_progress_specific(id_request)

    @staticmethod
    def list_district_progress(id_acc):
        return DistrictServices.list_district_progress(id_acc)

    @staticmethod
    def list_district_progress_specific(id_acc, id_request):
        return DistrictServices.list_district_progress_specific(id_acc, id_request)

    @staticmethod
    def list_ward_progress(id_acc):
        return WardServices.list_ward_progress(id_acc)

    @staticmethod
    def list_ward_progress_specific(id_acc, id_request):
        return WardServices.list_ward_progress_specific(id_acc, id_request)

    # @staticmethod
    # def send_mail(arr):

