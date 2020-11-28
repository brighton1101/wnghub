import datetime
from typing import List

from wnghub.model.model import BaseModel
from wnghub.model.filter import BaseFilter
from dataclasses import dataclass
from marshmallow import Schema, fields, pre_load, post_load, EXCLUDE


@dataclass
class Notification(BaseModel):
    """
    Model representing notifications received
    from Github's notifications endpoint.

    :see: https://docs.github.com/en/free-pro-team@latest/rest/reference/activity#notifications
    """

    title: str = ""
    repository: str = ""
    org: str = ""
    html_url: str = ""
    reason: str = ""
    is_pull: bool = False
    is_issue: bool = False
    updated_at: datetime.datetime = datetime.MINYEAR

    _pull_type = "PullRequest"
    _issue_type = "Issue"

    class NotificationSchema(Schema):
        title = fields.Str()
        repository = fields.Str()
        org = fields.Str()
        html_url = fields.Str()
        reason = fields.Str()
        is_pull = fields.Bool()
        is_issue = fields.Bool()
        updated_at = fields.DateTime()

        @pre_load
        def is_issue_or_pr(self, data, **kwargs):
            n_type = data.get("subject").get("type")
            if n_type == Notification._pull_type:
                data["is_pull"] = True
            elif n_type == Notification._issue_type:
                data["is_issue"] = True
            return data

        @pre_load
        def parse_title(self, data, **kwargs):
            data["title"] = data.get("subject").get("title")
            return data

        @pre_load
        def parse_repository_org(self, data, **kwargs):
            repo = data.get("repository")
            data["repository"] = repo.get("name")
            data["org"] = repo.get("owner").get("login")
            return data

        @pre_load
        def parse_html_url(self, data, **kwargs):
            api_url = data.get("subject").get("url")
            html_url = api_url.replace("api.", "", 1)
            data["html_url"] = html_url
            return data

        @post_load
        def get_notification(self, data, **kwargs):
            return Notification(**data)

    SCHEMA = NotificationSchema

    @staticmethod
    def load_from_json_str(res):
        n = Notification.SCHEMA()
        res = n.loads(res, many=True, unknown=EXCLUDE)
        return sorted(res, key=lambda x: x.updated_at, reverse=True)


class NotificationReasonsFilter(BaseFilter):
    """
    Filters notifications by reason. Either choose to
    supply a list of reasons to include results for, or
    exclude results from because of.

    By default will only return results provided in
    reasons.

    :see: https://docs.github.com/en/free-pro-team@latest/rest/reference/activity#notification-reasons  # noqa

    :param reasons: list of reasons
    :type reasons: List[str]
    :param exclude: whether to solely include or exclude
                    the notifications provided
    :param exclude: bool
    """

    def __init__(self, reasons: List[str], exclude: bool = False):
        self.reasons = set(reasons)
        self.exclude = exclude

    def include(self, obj: Notification) -> bool:
        if self.exclude is False and obj.reason in self.reasons:
            return True
        elif self.exclude is True and obj.reason not in self.reasons:
            return True
        return False


class NotificationPrIssuesFilter(BaseFilter):
    """
    Filters Notifications by whether they are pull
    requests, issues, or both.

    By default will exclude everything.

    :param get_prs: whether or not to include prs
    :type get_prs: bool
    :param get_issues: whether or not to include issues
    :type get_issues: bool
    """

    def __init__(self, get_prs: bool = False, get_issues: bool = False):
        self.get_prs = get_prs
        self.get_issues = get_issues

    def include(self, obj: Notification) -> bool:
        if self.get_prs and obj.is_pull:
            return True
        elif self.get_issues and obj.is_issue:
            return True
        return False


class NotificationReposFilter(BaseFilter):
    """
    Filters Notifications by repository name.

    By default will only include repos in list
    of repositories. Optionally, do the opposite
    and only exclude those in the repos list.

    :param repos: list of repositories to filter with
    :type repos: List[str]
    :param exclude: whether to exclude or include matches
    :type exclude: bool
    """

    def __init__(self, repos: List[str], exclude: bool = False):
        self.repos = set(repos)
        self.exclude = exclude

    def include(self, obj: Notification) -> bool:
        if obj.repository in self.repos and self.exclude:
            return False
        elif obj.repository in self.repos:
            return True
        elif self.exclude:
            return True
        return False


class NotificationOrgsFilter(BaseFilter):
    """
    Filters Notifications by org name.

    By default will only include orgs in list
    of repositories. Optionally, do the opposite
    and only exclude those in the list.

    :param orgs: list of orgs to filter with
    :type orgs: List[str]
    :param exclude: whether to exclude or include matches
    :type exclude: bool
    """

    def __init__(self, orgs: List[str], exclude: bool = False):
        self.orgs = set(orgs)
        self.exclude = False

    def include(self, obj: Notification) -> bool:
        if obj.org in self.orgs and self.exclude:
            return False
        elif obj.org in self.orgs:
            return True
        elif self.exclude:
            return True
        return False
