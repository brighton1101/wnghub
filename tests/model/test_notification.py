from wnghub.model.notification import Notification, NotificationReasonsFilter, NotificationPrIssuesFilter, NotificationReposFilter
from unittest.mock import Mock, MagicMock
import datetime


def test_load_pyghub():
    mock_pr = Mock()
    mock_pr.html_url = 'https://github.com/brighton1101/gcp-metadata-access-token'
    mock_notification = Mock()
    mock_notification.reason = 'HELLO'
    mock_notification.subject = Mock()
    mock_notification.subject.title = 'test'
    mock_notification.get_pull_request = MagicMock(return_value=mock_pr)
    mock_notification.subject.type = 'PullRequest'
    mock_notification.updated_at = datetime.MINYEAR
    res = Notification.load_from_pyghub(mock_notification)
    assert res.title == 'test'
    assert res.is_pull == True
    assert res.reason == 'HELLO'
    assert res.html_url == 'https://github.com/brighton1101/gcp-metadata-access-token'
    assert res.updated_at == datetime.MINYEAR
    assert res.is_issue == False
    assert res.org == 'brighton1101'
    assert res.repository == 'gcp-metadata-access-token'


def test_notification_reasons_filter_include():
    mock_notification = Mock()
    mock_notification.reason = 'HELLO WORLD'
    nr_filter = NotificationReasonsFilter(['HELLO WORLD'])
    res = nr_filter.apply([mock_notification])
    assert len(res) == 1
    assert res[0] == mock_notification


def test_notification_reasons_filter_exclude():
    mock_notification = Mock()
    mock_notification.reason = 'HELLO WORLD'
    nr_filter = NotificationReasonsFilter(['HELLO WORLD'], exclude=True)
    res = nr_filter.apply([mock_notification])
    assert len(res) == 0


def test_notification_pr_issues_filter_pr():
    mock_notification_pr = Mock()
    mock_notification_issue = Mock()
    mock_notification_pr.is_pull = True
    mock_notification_issue.is_pull = False
    mock_notification_pr.is_issue = False
    mock_notification_issue.is_issue = True
    npr_filter = NotificationPrIssuesFilter(get_prs=True)
    res = npr_filter.apply([mock_notification_pr, mock_notification_issue])
    assert len(res) == 1
    assert res[0] == mock_notification_pr


def test_notification_pr_issues_filter_issue():
    mock_notification_pr = Mock()
    mock_notification_issue = Mock()
    mock_notification_pr.is_pull = True
    mock_notification_issue.is_pull = False
    mock_notification_pr.is_issue = False
    mock_notification_issue.is_issue = True
    npr_filter = NotificationPrIssuesFilter(get_issues=True)
    res = npr_filter.apply([mock_notification_pr, mock_notification_issue])
    assert len(res) == 1
    assert res[0] == mock_notification_issue


def test_notification_repos_filter_include():
    mock_n_r1 = Mock()
    mock_n_r2 = Mock()
    mock_n_r1.repository = 'r1'
    mock_n_r2.repository = 'r2'
    nr_filter = NotificationReposFilter(['r1'])
    res = nr_filter.apply([mock_n_r1, mock_n_r2])
    assert len(res) == 1
    assert res[0] == mock_n_r1


def test_notification_repos_filter_exclude():
    mock_n_r1 = Mock()
    mock_n_r2 = Mock()
    mock_n_r1.repository = 'r1'
    mock_n_r2.repository = 'r2'
    nr_filter = NotificationReposFilter(['r1'], exclude = True)
    res = nr_filter.apply([mock_n_r1, mock_n_r2])
    assert len(res) == 1
    assert res[0] == mock_n_r2
