from datetime import datetime
from typing import Optional


class Notification(object):
    title: str = ''
    repository: str = ''
    org: str = ''
    html_url: str = ''
    reason: str = ''
    is_pull: bool = False
    is_issue: bool = False
    updated_at: Optional[datetime] = None

    @staticmethod
    def load_from_pyghub(notif):
        """
        Helper method to load `Notification` from
        `github.Notification` object supplied by
        `PyGithub` response

        :param notif: notification to convert
        :type notif: `github.Notification`
        :return: Notification
        """
        n = Notification()
        n.title = notif.subject.title
        n.html_url = notif.get_pull_request().html_url
        n.reason = notif.reason
        if notif.subject.type == 'PullRequest':
            n.is_pull = True
        elif notif.subject.type == 'Issue':
            n.is_issue = True
        n.updated_at = notif.updated_at
        try:
            n.repository = n.html_url.split('/')[4]
        except IndexError:
            pass
        try:
            n.org = n.html_url.split('/')[3]
        except IndexError:
            pass
        return n
