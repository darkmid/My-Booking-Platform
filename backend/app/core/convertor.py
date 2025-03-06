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

def prepare_reference_fields(update_dict, field_mappings):
    result = update_dict.copy()
    
    for field_name, (model_class, error_msg) in field_mappings.items():
        if field_name in result:
            field_id = result[field_name]
            obj = model_class.objects(id=field_id).first_or_404(error_msg)
            result[field_name] = obj
    
    return result