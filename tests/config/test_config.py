from wnghub.config.config import Config
import pytest
from unittest.mock import MagicMock


def test_set_auth_success():
    a = Config()
    a.write = MagicMock(return_value=None)
    a.auth_token = "hello world"
    a.set_auth(auth_token="yay")
    a.write.assert_called_once()
    assert a.auth_token == "yay"
