import pandas as pd
import openpyxl

from flask import send_file
from flask_restful import Resource
from src.models.cityProvinceDb import CityDb
def to_dict(row):
    if row is None:
        return None

    rtn_dict = dict()
    keys = row.__table__.columns.keys()
    for key in keys:
        rtn_dict[key] = getattr(row, key)
    return rtn_dict


class TestExcel(Resource):

    def get(self):
        data = CityDb.find_all()
        data_list = [to_dict(item) for item in data]
        df = pd.DataFrame(data_list)
        filename = "../open.xlsx"

        writer = pd.ExcelWriter(filename)
        df.to_excel(writer, sheet_name='Registrados')
        writer.save()

        return send_file(filename)