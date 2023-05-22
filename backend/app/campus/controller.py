from flask import request
from flask_restx import Namespace,Resource

from app.exceptions.database_exceptions import DuplicateRecord
from .model import Campus
from .schema import CampusListSchema, CampusSchema
from app.user import permission_required
from app.campus.service import campus_service

api = Namespace("campus")

@api.route("")
class CampusListApi(Resource):
    def get(self):
        campus_list = list(Campus.objects())
        print(campus_list)
        return CampusListSchema.from_orm(campus_list)
    
    @permission_required("campus_admin")
    def post(self):
        request_data = request.json
        if Campus.objects(name=request_data["name"]):
            raise DuplicateRecord("Campus already exists")
        campus=Campus(**request_data)
        campus=campus_service().register_campus(campus)
        return CampusSchema.from_orm(campus),201
