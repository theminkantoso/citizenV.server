class Services():
    @staticmethod
    def convert_to_json_dict(arr):
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
