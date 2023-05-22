import datetime
import json

from pydantic import BaseModel,SecretStr
from uuid import UUID

class CustomEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,datetime.datetime):
            return obj.isoformat()
        if isinstance(obj,SecretStr):
            return None
        if isinstance(obj,BaseModel):
            return obj.dict(exclude_defaults=True)
        if isinstance(obj, UUID):
            return str(obj)
        else:
            return super().default(obj)