from src.models.citizenDb import CitizenDb


class StatisticsService():

    @staticmethod
    def population(id, role):
        if id == 'A1' and role == 1:
            return int(CitizenDb.get_population_entire())
        elif role == 2:
            return int(CitizenDb.get_population_city(id))
        elif role == 3:
            return int(CitizenDb.get_population_district(id))
        elif role == 4:
            return int(CitizenDb.get_population_ward(id))

    @staticmethod
    def stat_sex(id, role):
        if id == 'A1' and role == 1:
            return CitizenDb.get_stats_sex_entire()
        elif role == 2:
            return CitizenDb.get_stats_sex_city(id)
        elif role == 3:
            return CitizenDb.get_stats_sex_district(id)
        elif role == 4:
            return CitizenDb.get_stats_sex_ward(id)

    @staticmethod
    def stat_edu(id, role):
        if id == 'A1' and role == 1:
            return CitizenDb.get_stats_edu_entire()
        elif role == 2:
            return CitizenDb.get_stats_edu_city(id)
        elif role == 3:
            return CitizenDb.get_stats_edu_district(id)
        elif role == 4:
            return CitizenDb.get_stats_edu_ward(id)

    @staticmethod
    def stat_marital(id, role):
        if id == 'A1' and role == 1:
            return CitizenDb.get_marital_status_entire()
        elif role == 2:
            return CitizenDb.get_stats_edu_city(id)
        elif role == 3:
            return CitizenDb.get_marital_status_district(id)
        elif role == 4:
            return CitizenDb.get_marital_status_ward(id)
