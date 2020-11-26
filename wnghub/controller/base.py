from wnghub.config.config import Config


class BaseController(object):
    def __init__(self, config: Config):
        self.config = config
