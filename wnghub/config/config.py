from typing import Optional
from marshmallow import Schema, fields, post_load, validates_schema
from wnghub.config.base import BaseConfig


class Config(BaseConfig):
    """
    Configuration for application
    """

    auth_token: Optional[str] = ""

    DEFAULT_CONFIG_PATH = "~/wnghub.config"

    class ConfigSchema(Schema):
        auth_token = fields.Str(allow_none=True)

        @post_load
        def get_config_obj(self, data, **kwargs):
            return Config(**data)

    SCHEMA = ConfigSchema

    def __init__(
        self,
        auth_token: Optional[str] = "",
    ):
        """
        Constructor to initialize Config. Note that
        this should NOT be called directly.

        :param username: Github username
        :type username: Optional[str]
        :param password: Github password
        :type password: Optional[str]
        :param auth_token: Github auth token
        :type auth_token: Optional[str]
        """
        self.auth_token = auth_token
        BaseConfig.__init__(self)

    def set_auth(self, auth_token=None, username=None, password=None):
        """
        Sets auth for Config. Allows either (username, password) OR auth_token.
        Mutually exclusive.

        :param auth_token: Github auth token
        :type auth_token: Optional[str]
        :param username: Github username
        :type username: Optional[str]
        :param password: Github password
        :type password: Optional[str]
        """
        self.auth_token = auth_token
        self.write()

    def get_credentials(self):
        """
        Gets credentials from config

        :return: tuple with the following:
                (possible token, possible(user, pw))
        """
        if self.auth_token is not None:
            return (self.auth_token, None)
        else:
            return (None, (self.username, self.password))

    @staticmethod
    def read():
        """
        Initializes config if it doesn't exist. Loads
        Config from file.

        :return: Config instance
        """
        return BaseConfig._read(Config)
