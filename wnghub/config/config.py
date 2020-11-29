from typing import Optional, List
from datetime import datetime
from dataclasses import dataclass
from marshmallow import Schema, fields, post_load
from wnghub.config.base import BaseConfig


@dataclass
class Config(BaseConfig):
    """
    Configuration for application
    """

    auth_token: Optional[str] = ""
    show_num_results: int = 5
    only_include_repos: Optional[List[str]] = None
    only_include_orgs: Optional[List[str]] = None
    only_include_reasons: Optional[List[str]] = None
    exclude_repos: Optional[List[str]] = None
    exclude_orgs: Optional[List[str]] = None
    exclude_reasons: Optional[List[str]] = None
    show_read_results: bool = False
    only_include_participating: bool = False
    only_include_since: Optional[datetime] = None
    only_include_before: Optional[datetime] = None
    include_issues: bool = True
    include_prs: bool = True

    DEFAULT_CONFIG_PATH = "~/wnghub.config"

    class ConfigSchema(Schema):
        auth_token = fields.Str(allow_none=True)
        show_num_results = fields.Int(allow_none=True)
        only_include_repos = fields.List(fields.Str(), allow_none=True)
        only_include_reasons = fields.List(fields.Str(), allow_none=True)
        only_include_orgs = fields.List(fields.Str(), allow_none=True)
        exclude_repos = fields.List(fields.Str(), allow_none=True)
        exclude_orgs = fields.List(fields.Str(), allow_none=True)
        exclude_reasons = fields.List(fields.Str(), allow_none=True)
        show_read_results = fields.Bool(allow_none=True)
        only_include_participating = fields.Bool(allow_none=True)
        only_include_since = fields.DateTime(allow_none=True)
        only_include_before = fields.DateTime(allow_none=True)
        include_issues = fields.Bool(allow_none=True)
        include_prs = fields.Bool(allow_none=True)

        @post_load
        def get_config_obj(self, data, **kwargs):
            return Config(**data)

    SCHEMA = ConfigSchema

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
