from marshmallow import Schema
from typing import Optional
from abc import ABC


class BaseModel(ABC):
    SCHEMA: Optional[Schema] = None
