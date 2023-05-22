from typing import List

from flask_jwt_extended import get_current_user

from app.core.service import BaseService
from .model import Campus,User, get_hashed_password
from mongoengine.errors import NotUniqueError
from app.exceptions.database_exceptions import DuplicateRecord
from app.exceptions.permission_exceptions import PermissionDenied

class UserService(BaseService):
    def __init__(self, user) -> None:
        super().__init__(UserService.__name__, user)

    def list_users(self, user_type: str = None, campus: Campus = None) -> List[User]:
        self.logger.info("Fetching users")
        querys = {}
        if user_type is not None:
            querys["_cls"] = "User." + user_type.lower().capitalize()
        if campus is not None:
            querys["campus"] = campus
        return list(User.objects(**querys))
    
    def register_user(self, user: User):
        try:
            user.password = get_hashed_password(user.password)
            user.save()
            return user
        except NotUniqueError:
            raise DuplicateRecord("User already exists")
    
    def get_user(self, username) -> User:
        if self.user.username == username or (
            self.user._cls == "User.Admin" and "user_admin" in self.user.permissions
        ):
            return User.objects(username=username).first_or_404("User not exists")
        else:
            raise PermissionDenied()

    def delete_user(self, username):
        if self.user.username == username or (
            self.user._cls == "User.Admin" and "user_admin" in self.user.permissions
        ):
            user = User.objects(username=username).first_or_404("User not exists")
            user.delete()
        else:
            raise PermissionDenied()

    def update_user(self, username: str, **kwargs):
        if "password" in kwargs:
            kwargs["password"] = get_hashed_password(kwargs["password"])

        if self.user._cls == "User.Admin" and "sys_owner" in self.user.permissions:
            self.logger.info("Update user as sys admin")
            user = User.objects(username=username).first_or_404("User not exists")
            user.update_from_dict(**kwargs)
        elif self.user.username == username or (
            self.user._cls == "User.Admin" and "user_admin" in self.user.permissions
        ):
            self.logger.info("Update user as user admin or self")
            user = User.objects(username=username).first_or_404("User not exists")
            kwargs.pop("permissions", None)
            user.update_from_dict(**kwargs)
    
    def update_password(self, username: str, **kwargs):
        if "password" in kwargs:
            kwargs["password"] = get_hashed_password(kwargs["password"])

        if User.objects(username=username).first_or_404("User not exists"):
            user = User.objects(username=username).first_or_404("User not exists")
            user.update_from_dict(**kwargs)


def user_service():
    return UserService(get_current_user())

def unauthorized_user_service():
    return UserService(None)