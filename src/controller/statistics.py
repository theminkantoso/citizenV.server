from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.core.auth import authorized_required
from src.services.statisticsService import StatisticsService


class Statistics(Resource):

    @jwt_required()
    @authorized_required(roles=[1, 2, 3, 4])
    def get(self):
        id_acc = get_jwt_identity()
        claims = get_jwt()
        role = claims["role"]
        if role == 1:
            population = StatisticsService.population('A1', 1)
            stat_sex = StatisticsService.stat_sex('A1', 1)
            marital = StatisticsService.stat_marital('A1', 1)
            edu = StatisticsService.stat_edu('A1', 1)
            group_age = StatisticsService.stat_group_age('A1', 1)
        elif role == 2 or role == 3 or role == 4:
            population = StatisticsService.population(id_acc, role)
            stat_sex = StatisticsService.stat_sex(id_acc, role)
            marital = StatisticsService.stat_marital(id_acc, role)
            edu = StatisticsService.stat_edu(id_acc, role)
            group_age = StatisticsService.stat_group_age(id_acc, role)
        else:
            return {"msg": "Something went wrong"}, 404

        if stat_sex:
            stat_sex_json = StatisticsService.convert_to_dict_sex(stat_sex)
        if marital:
            marital_json = StatisticsService.convert_to_dict_marital(marital)
        if edu:
            edu_json = StatisticsService.convert_to_dict_edu(edu)
        if group_age:
            group_age_json = StatisticsService.convert_to_dict_group_age(group_age)
        ret_dict = {}
        if stat_sex_json and marital_json and edu_json:
            ret_dict = {**stat_sex_json, **marital_json, **edu_json, **group_age_json}
        ret_dict["population"] = population
        if ret_dict:
            return ret_dict, 200
        return {}, 200

    # Phân tích citizen theo từng nhóm vùng
    @jwt_required()
    @authorized_required(roles=[1, 2, 3, 4])
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("areas", action='append')

        id_acc = get_jwt_identity()
        claims = get_jwt()
        role = claims["role"]

        # input id arr, sửa ở đây
        data = parser.parse_args()
        arr = data["areas"]
        print(arr)
        len_first = len(arr[0])
        for i in arr:
            if not StatisticsService.check_request_two_digit(i) or len(i) != len_first:
                return {"msg": "invalid input"}, 400
            if not StatisticsService.check_valid_request_role(i, role):
                return {"msg": "not authorized"}, 403
        # if 1 <= role <= 4:
        #     for i in arr:
                # if not StatisticsService.check_valid_request(id_acc, i):
                #     return {"msg": "not authorized"}, 403
        if 1 <= role <= 4:
            population = StatisticsService.populations(arr)
            stat_sex = StatisticsService.stat_sexs(arr)
            marital = StatisticsService.stat_maritals(arr)
            edu = StatisticsService.stat_edus(arr)
            group_age = StatisticsService.stat_group_ages(arr)
        else:
            return {"msg": "Something went wrong"}, 404
        edu_json = ''
        stat_sex_json = ''
        marital_json = ''
        group_age_json = ''
        if stat_sex:
            stat_sex_json = StatisticsService.convert_to_dict_sex(stat_sex)
        if marital:
            marital_json = StatisticsService.convert_to_dict_marital(marital)
        if edu:
            edu_json = StatisticsService.convert_to_dict_edu(edu)
        if group_age:
            group_age_json = StatisticsService.convert_to_dict_group_age(group_age)
        ret_dict = {}
        if stat_sex_json and marital_json and edu_json:
            ret_dict = {**stat_sex_json, **marital_json, **edu_json, **group_age_json}
        ret_dict["population"] = population
        if ret_dict:
            return ret_dict, 200
        return {}, 200


class StatisticsSpecific(Resource):

    @jwt_required()
    @authorized_required(roles=[1, 2, 3, 4])
    def get(self, id):
        id_acc = get_jwt_identity()
        claims = get_jwt()
        role = claims["role"]
        id_request = id
        if not StatisticsService.check_request_two_digit(id_request):
            return {"msg": "invalid input"}, 400
        if not StatisticsService.check_valid_request_role(id_request, role):
            return {"msg": "not authorized"}, 403
        if 2 <= role <= 4:
            if not StatisticsService.check_valid_request(id_acc, id_request):
                return {"msg": "not authorized"}, 403
        if 1 <= role <= 4:
            population = StatisticsService.population(id_request, StatisticsService.gen_index_request(id_request))
            stat_sex = StatisticsService.stat_sex(id_request, StatisticsService.gen_index_request(id_request))
            marital = StatisticsService.stat_marital(id_request, StatisticsService.gen_index_request(id_request))
            edu = StatisticsService.stat_edu(id_request, StatisticsService.gen_index_request(id_request))
            group_age = StatisticsService.stat_group_age(id_request, StatisticsService.gen_index_request(id_request))
            name = StatisticsService.get_name(id_request, StatisticsService.gen_index_request(id_request))
        else:
            return {"msg": "Something went wrong"}, 404
        edu_json = ''
        if stat_sex:
            stat_sex_json = StatisticsService.convert_to_dict_sex(stat_sex)
        if marital:
            marital_json = StatisticsService.convert_to_dict_marital(marital)
        if edu:
            edu_json = StatisticsService.convert_to_dict_edu(edu)
        if group_age:
            group_age_json = StatisticsService.convert_to_dict_group_age(group_age)
        ret_dict = {}
        if stat_sex_json and marital_json and edu_json:
            ret_dict = {**stat_sex_json, **marital_json, **edu_json, **group_age_json}
        ret_dict["population"] = population
        ret_dict["name"] = name
        if ret_dict:
            return ret_dict, 200
        return {}, 200
