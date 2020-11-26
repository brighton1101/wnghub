from pathlib import Path
from typing import Optional
from marshmallow import Schema


class BaseConfig(object):
    DEFAULT_CONFIG_PATH: str = ""
    SCHEMA: Schema = ...

    def config_path(self) -> Path:
        """
        Gets config for class

        :return: `pathlib.Path`
        """
        return config_path(self.DEFAULT_CONFIG_PATH)

    def write(self):
        """
        Writes config instance to file
        """
        resolved_path = self.config_path()
        schema = self.SCHEMA()
        result = schema.dumps(self)
        resolved_path.write_text(result)

    @staticmethod
    def read():
        raise NotImplementedError("Cannot call read from base class")

    @staticmethod
    def _read(cls, config_location: Optional[str] = None):
        """
        Loads instance of `cls` (a subclass of BaseConfig)
        with the appropriate schema and contents

        :param cls: Class to load config to
        :type cls: Subclass of `BaseConfig`
        :param config_location: Where to load config from. By default,
                                the class' DEFAULT_CONFIG_PATH
        :type config_location: str
        :return: instance of `cls`
        """
        if config_location is None:
            config_location = cls.DEFAULT_CONFIG_PATH
        resolved_path = config_path(config_location)
        resolved_path.touch(exist_ok=True)
        config_contents = resolved_path.read_text()
        if config_contents is "":
            config_contents = "{}"
            resolved_path.write_text(config_contents)
        schema = cls.SCHEMA()
        return schema.loads(config_contents)


def config_path(path_to_file=""):
    return Path(path_to_file).expanduser()
