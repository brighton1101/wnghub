from wnghub.client.github import PyGithubClient
from unittest.mock import Mock, MagicMock, patch
from wnghub.model.notification import Notification


@patch('wnghub.client.github.Notification')
def test_get_notifications(mock_notification):
    mock_gh_notification = Mock()
    client = PyGithubClient('test 123')
    client._notifications = MagicMock(return_value=[mock_gh_notification])
    client.get_notifications()
    mock_notification.load_from_pyghub.assert_called_once_with(mock_gh_notification)
