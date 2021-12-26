import pandas as pd
import openpyxl

from UliPlot.XLSX import auto_adjust_xlsx_column_width

from flask import send_file
from flask_restful import Resource
from src.services.excelService import ExcelServices
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.core.auth import authorized_required


class TestExcel(Resource):

    @jwt_required()
    @authorized_required(roles=[3, 4])
    def get(self):
        id_acc = get_jwt_identity()
        claims = get_jwt()
        role = claims["role"]
        data = ExcelServices.get_citizen(id_acc, role)
        data_list = [ExcelServices.to_dict(item) for item in data]
        df = pd.DataFrame(data_list)
        filename = "../danso.xlsx"

        writer = pd.ExcelWriter(filename)
        df.to_excel(writer, sheet_name='DanSo', na_rep='')
        auto_adjust_xlsx_column_width(df, writer, sheet_name="DanSo", margin=3)
        writer.save()

        return send_file(filename, download_name="Dan So", attachment_filename="Dan So")
