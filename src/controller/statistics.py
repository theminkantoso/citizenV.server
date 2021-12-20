from flask_restful import Resource
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
        id_acc_len = len(id_acc)
        if role == 1:
            population = StatisticsService.population('A1', 1)
            stat_sex = StatisticsService.stat_sex('A1', 1)
        elif id_acc_len == 2:
            population = StatisticsService.population(id_acc, 2)
            stat_sex = StatisticsService.stat_sex(id_acc, 2)
        elif id_acc_len == 4:
            population = StatisticsService.population(id_acc, 3)
            stat_sex = StatisticsService.stat_sex(id_acc, 3)
        elif id_acc_len == 6:
            population = StatisticsService.population(id_acc, 4)
            stat_sex = StatisticsService.stat_sex(id_acc, 4)
        else:
            return {"message": "Something went wrong"}, 404
#
#
#
