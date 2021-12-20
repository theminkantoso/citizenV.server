from src.services.citizen import CitizenServices


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
