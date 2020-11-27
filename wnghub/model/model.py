from marshmallow import Schema
from typing import Optional

class BaseModel(object):
    SCHEMA: Optional[Schema] = None
    pass