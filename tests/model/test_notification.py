from wnghub.model.notification import Notification
from unittest.mock import Mock, MagicMock
import datetime


def test_load_pyghub():
    mock_pr = Mock()
    mock_pr.url = 'www.test.com'
    mock_notification = Mock()
    mock_notification.reason = 'HELLO'
    mock_notification.subject = Mock()
    mock_notification.subject.title = 'test'
    mock_notification.get_pull_request = MagicMock(return_value=mock_pr)
    mock_notification.subject.type = 'PullRequest'
    mock_notification.updated_at = datetime.MINYEAR
    res = Notification.load_from_pyghub(mock_notification)
    assert res.title == 'test'
    assert res.is_pull is True
    assert res.reason == 'HELLO'
    assert res.html_url == 'www.test.com'
    assert res.updated_at == datetime.MINYEAR
    assert res.is_issue is False
