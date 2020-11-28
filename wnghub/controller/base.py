from wnghub.config.config import Config
from abc import ABC


class BaseController(ABC):
    """
    Base controller class for application. By default,
    all controllers should have access to the config.

    :param config: application config
    :type config: Config
    """
    def __init__(self, config: Config):
        self.config = config
