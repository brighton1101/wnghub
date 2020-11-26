from typing import Optional
from marshmallow import Schema, fields, post_load, validates_schema
from wnghub.config.base import BaseConfig


class Config(BaseConfig):
    """
    Configuration for application
    """

    username: Optional[str] = None
    password: Optional[str] = None
    auth_token: Optional[str] = None

    DEFAULT_CONFIG_PATH = "~/wnghub.config"

    class ConfigSchema(Schema):
        username = fields.Str(allow_none=True)
        password = fields.Str(allow_none=True)
        auth_token = fields.Str(allow_none=True)

        @validates_schema
        def validate_auth(self, data, **kwargs):
            _verify_auth(
                data.get("auth_token"), data.get("username"), data.get("password")
            )

        @post_load
        def get_config_obj(self, data, **kwargs):
            return Config(**data)

    SCHEMA = ConfigSchema

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        auth_token: Optional[str] = None,
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
        self.username = username
        self.password = password
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
        _verify_auth(auth_token, username, password)
        self.auth_token = auth_token
        self.username = username
        self.password = password
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


def _username_pw_provided(username: Optional[str], password: Optional[str]) -> bool:
    if bool(username is None) != bool(password is None):
        raise ValueError(
            "If username or password is provided, " "both must be provided"
        )
    if username is None:
        return False
    return True


def _verify_auth(auth_token, username, password):
    username_pw_provided = _username_pw_provided(username, password)
    if username_pw_provided and auth_token is not None:
        raise ValueError("Cannot provide both username and password, " "and auth token")
