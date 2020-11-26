from typing import Optional

from wnghub.controller.base import BaseController


class ConfigController(BaseController):
    """
    Controller to manage getting and setting configs
    for end user.

    :constructor:
    :param config: the config instance to manage
    :type config: `wnghub.config.config.Config`
    """

    """
    Register valid config fields below that are
    allowed to be accessed from controller.
    """
    _valid_config_fields = ["auth_token"]

    """
    Register config fields that should not be
    set directly below. Map them to a separate
    command to set config field directly.
    """
    _disallow_set_directly = {"auth_token": "set-auth"}

    """
    Register any fields that need preprocessing
    below. Key is name of the field and the value
    is a function that takes exactly one arg to
    preprocess the field.

    Example 'max_results': lambda x: int(x)
    """
    _preprocess_mappings = {}

    def get(self, field_name: str):
        """
        Gets attribute based on provided field name.

        :param field_name: field name to lookup in config
        :type field_name: str
        :return: any
        """
        self._verify_valid_field(field_name)
        self.config.__getattribute__(field_name)  # NOQA

    def set(self, field_name: str, value):
        """
        Sets attribute based on provided field name and value.

        Will preprocess field using function provided in
        `preprocess_mappings` if it exists.

        :param field_name: field name to set in config
        :type field_name: str
        :param value: value to be set in config
        """
        self._verify_valid_field(field_name)
        if field_name in self._disallow_set_directly:
            raise Exception(
                "Field: {} is not allowed to be set directly. Please use {} instead.".format(
                    field_name, self._disallow_set_directly.get(field_name)
                )
            )
        if field_name in self._preprocess_mappings:
            value = self._preprocess_mappings.get(field_name)(value)
        self.config.__setattr__(field_name, value)  # NOQA
        self.config.write()

    def set_auth(self, auth_token: Optional[str] = None):
        """
        Sets auth token in config. If auth_token is None,
        it will be removed from config.

        :param auth_token: auth token to be set
        :type auth_token: Optional[str]
        """
        self.config.set_auth(auth_token=auth_token)

    def _verify_valid_field(self, field_name: str):
        """
        Verifies that field is available in config.

        :param field_name: field to check in config
        :type field_name: str
        :raises Exception: if field not in config
        """
        if field_name not in self._valid_config_fields:
            raise Exception("Field: {} is not a valid config field".format(field_name))
