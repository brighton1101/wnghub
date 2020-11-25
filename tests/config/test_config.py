from wnghub.config.config import Config
import pytest
from unittest.mock import MagicMock

def test_set_auth_username_missing_pw():
    a = Config()
    a.write = MagicMock(return_value=None)
    with pytest.raises(ValueError):
        a.set_auth(username='testing')
    a.write.assert_not_called()


def test_set_auth_password_missing_username():
    a = Config()
    a.write = MagicMock(return_value=None)
    with pytest.raises(ValueError):
        a.set_auth(password='testing')
    a.write.assert_not_called()


def test_set_auth_auth_token_and_username():
    a = Config()
    a.write = MagicMock(return_value=None)
    with pytest.raises(ValueError):
        a.set_auth(username='testing', auth_token='hello world')
    a.write.assert_not_called()


def test_set_auth_success():
    a = Config()
    a.write = MagicMock(return_value=None)
    a.auth_token = 'hello world'
    a.set_auth(username='testing', password='testing')
    assert a.username == 'testing'
    assert a.password == 'testing'
    assert a.auth_token == None
    a.write.assert_called_once()
