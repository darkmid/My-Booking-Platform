
from flask_jwt_extended import get_current_user
from app.core.service import BaseService
from app.campus.model import Campus
from mongoengine.errors import NotUniqueError
from app.exceptions.database_exceptions import DuplicateRecord


class CampusService(BaseService):
    def __init__(self, user) -> None:
        super().__init__(CampusService.__name__, user)

    def register_campus(self,campus:Campus):
        try:
            campus.save()
            return campus
        except NotUniqueError:
            raise DuplicateRecord("Campus already exists")
        
def campus_service():
    return CampusService(get_current_user())