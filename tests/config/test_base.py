from wnghub.config.base import BaseConfig
from unittest.mock import MagicMock, patch
from marshmallow import Schema, fields
from pathlib import Path
import json


def test_write():
    class MockConfig(BaseConfig):
        def read():
            pass
    c = MockConfig()
    class MockSchema(Schema):
        pass
    mock_schema = MockSchema()
    mock_schema.dumps = MagicMock(return_value='{}')
    c.SCHEMA = MagicMock(return_value=mock_schema)
    with patch.object(Path, 'write_text') as mock_writes:
        c.write()
    mock_schema.dumps.assert_called_once_with(c)
    mock_writes.assert_called_once_with('{}')


def test_read_file_not_exists():
    mock_file_contents = ''
    class MockSchema(Schema):
        hello = fields.Str()
    class MockConfig(BaseConfig):
        DEFAULT_CONFIG_PATH = '~/hello'
        SCHEMA = MockSchema
        hello = None
    with patch.object(Path, 'read_text') as read_text, \
        patch.object(Path, 'touch') as touch, \
        patch.object(Path, 'write_text') as write_text:
        read_text.return_value = mock_file_contents
        res = MockConfig._read(MockConfig)
    assert len(res) == 0


def test_read_file_exists():
    mock_file_contents = json.dumps({
        'hello': 'world'
    })
    class MockSchema(Schema):
        hello = fields.Str()
    class MockConfig(BaseConfig):
        DEFAULT_CONFIG_PATH = '~/hello'
        SCHEMA = MockSchema
        hello = None
    with patch.object(Path, 'read_text') as read_text, \
        patch.object(Path, 'touch') as touch, \
        patch.object(Path, 'write_text') as write_text:
        read_text.return_value = mock_file_contents
        res = MockConfig._read(MockConfig)
    assert res.get('hello') == 'world'
    assert len(res) == 1
