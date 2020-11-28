from typing import List
from wnghub.model.model import BaseModel
from abc import ABC, abstractmethod


class BaseFilter(ABC):
    """
    `BaseFilter` used as a template for creating
    model filters within application.
    """

    def apply(self, objs: List[BaseModel]) -> List[BaseModel]:
        """
        Applies filter to list of model classes.

        :param objs: list of models
        :type objs: subclasses of `BaseModel`
        :return: List[BaseModel]
        """
        res = []
        for obj in objs:
            if self.include(obj):
                res.append(obj)
        return res

    @abstractmethod
    def include(self, obj: BaseModel) -> bool:
        pass


class AggregateFilter(BaseFilter):
    """
    Aggregates filter objects. Allows you to apply
    filter to list of objects.

    :param filters: list of filters to apply
    :type filters: List[BaseFilter]
    """

    def __init__(self, filters: List[BaseFilter]):
        self.filters = filters

    def include(self, obj: BaseModel) -> bool:
        should_include = True
        for f in self.filters:
            should_include = should_include and f.include(obj)
        return should_include
