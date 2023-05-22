from typing import List
from app.core.type import MongoModel,PydanticObjectId,MongoListModel,AllOptional
from pydantic import SecretStr, validator
from datetime import datetime

from app.course.schema import CourseBasicInfoSchema

#User Schema(Basic Schema)
class UserCampusSchema(MongoModel):
    id: PydanticObjectId
    name: str

class UserSchema(MongoModel):
    id:PydanticObjectId
    username:str
    password:SecretStr
    display_name:str
    telephone:str
    campus:PydanticObjectId
    created_at:datetime
    user_type: str

    @validator("user_type")
    def extract_user_type(cls, v):
        return v.split(".")[-1].lower()

    class Config:
        orm_mode = True
        fields = {"user_type": "_cls"}


class UserCreateSchema(MongoModel):
    username: str
    password: str
    display_name: str
    telephone: str
    campus: PydanticObjectId


class UserPutSchema(MongoModel, metaclass=AllOptional):
    password: str
    display_name: str
    telephone: str

class UserListSchema(MongoListModel):
    __root__: List[UserSchema]

#Student Schema
class StudentSchema(UserSchema):
    wx: str = None
    uni: str = None
    enrolled_courses: List[CourseBasicInfoSchema]
    
class StudentCreateSchema(UserCreateSchema):
    wx: str = None
    uni: str =None


class StudentPutSchema(UserPutSchema, metaclass=AllOptional):
    wx: str
    uni: str

class StudentListSchema(MongoListModel):
    __root__: List[StudentSchema]


#Admin Schema
class AdminSchema(UserSchema):
    permissions: List[str]


class AdminCreateSchema(UserCreateSchema):
    permissions: List[str]


class AdminPutSchema(UserPutSchema, metaclass=AllOptional):
    permissions: List[str]

class AdminListSchema(MongoListModel):
    __root__: List[AdminSchema]

#Teacher Schema
class TeacherSchema(UserSchema):
    abn: str = None


class TeacherCreateSchema(UserCreateSchema):
    abn: str = None


class TeacherPutSchema(UserPutSchema, metaclass=AllOptional):
    abn: str = None

class TeacherListSchema(MongoListModel):
    __root__: List[TeacherSchema]