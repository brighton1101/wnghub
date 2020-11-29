from dataclasses import dataclass
from typing import Any, Optional

from wnghub.config.config import Config


@dataclass
class Kwarg:
    """
    Wrapper around each Kwarg.

    :param kwarg_name: name of kwarg
    :type kwarg_name: str
    :param config_field_name: name of value in config
    :type config_field_name: str
    :param default_value: the default value to return if not in config
    :type default_value: Optional[Any]
    """

    kwarg_name: str
    config_field_name: str
    default_value: Optional[Any] = None


class KwargsReconciler(object):
    """
    A class to help reconcile missing kwargs with config and
    default values.

    :param *args: Tuple of Kwargs passed in as positional arguments
    :type *args: Tuple[Kwarg]
    :param config: optional config to pass in
    :type config: Config
    """

    def __init__(self, *args: Kwarg, config: Config = None):
        self.kwargs = dict([(arg.kwarg_name, arg) for arg in args])
        self.config = config

    def reconcile(self, kwarg_name: str, config: Config = None):
        """
        Reconcile the kwarg from the kwarg name. Priority is
        first given to the config value, then to the default
        value.

        :param kwarg_name: the name of the kwarg
        :type kwarg_name: str
        :param config: optional config to pass in
        :type config: Config
        :return: appropriate value for kwarg
        """
        config = config or self.config
        kwarg = self.kwargs.get(kwarg_name)
        config_val = None
        if config is not None:
            try:
                config_val = config.get(kwarg.config_field_name)
            except AttributeError:
                pass
        if config_val is None:
            return kwarg.default_value
        return config_val
