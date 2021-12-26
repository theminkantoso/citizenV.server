from io import BytesIO
from flask import send_file
from flask_restful import Resource
from src.models.fileDb import FileDb
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from src.core.auth import authorized_required


class File(Resource):

    @jwt_required()
    @authorized_required(roles=[4])
    def get(self):
        file = FileDb.file()[0]
        return send_file(file, as_attachment=True, mimetype='application/pdf', download_name=file)


