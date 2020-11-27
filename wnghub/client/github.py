from typing import Optional, List
from datetime import datetime
from functools import lru_cache
from requests import request

from wnghub.model.notification import Notification


class BaseGithubClient(object):

    auth_token: str = ""

    def __init__(self, auth_token: str):
        self.auth_token = auth_token

    def get_notifications(
        self,
        all: bool = False,
        participating: bool = False,
        since: Optional[datetime] = None,
        before: Optional[datetime] = None,
        per_page: int = None,
        page: int = 1,
    ) -> List[Notification]:
        raise NotImplementedError("Cannot be called directly from base client")


class GithubApiClient(BaseGithubClient):

    NOTIFICATIONS_URL = "https://api.github.com/notifications"

    @lru_cache(maxsize=None)
    def get_notifications(
        self,
        all: bool = False,
        participating: bool = False,
        since: Optional[datetime] = None,
        before: Optional[datetime] = None,
        per_page: int = 10,
        page: int = 1,
    ) -> List[Notification]:
        raw_res = self._notifications(
            all=all, participating=participating, since=since, before=before, per_page=per_page, page=page)
        return Notification.load_from_json_str(raw_res)

    @lru_cache(maxsize=None)
    def _notifications(
        self,
        all: bool = False,
        participating: bool = False,
        since: Optional[datetime] = None,
        before: Optional[datetime] = None,
        page: int = 1,
        per_page: int = 10,
    ):
        headers = {
            "Authorization": "token {}".format(self.auth_token),
            "accept": "application/vnd.github.v3+json",
        }
        params = {
            "all": "true" if all else "false",
            "participating": "true" if participating else "false",
            "page": page,
            "per_page": per_page
        }
        if since is not None:
            params['since'] = since.isoformat()
        if before is not None:
            params['before'] = before.isoformat()
        if per_page > 100:
            raise Exception(
                "Github API support maximum 100 notifications per page for api calls"
            )
        res = request("GET", self.NOTIFICATIONS_URL, headers=headers, params=params)
        return res.text


class PyGithubClient(BaseGithubClient):
    from github import Github, GithubObject

    _github = None

    @property
    def github(self):
        if self._github is None:
            self._github = Github(self.auth_token)
        return self._github

    @lru_cache(maxsize=None)
    def get_notifications(
        self,
        all: bool = False,
        participating: bool = False,
        since: Optional[datetime] = None,
        before: Optional[datetime] = None,
        per_page: int = 5,
        page: int = 1,
    ) -> List[Notification]:
        """
        Retrieves users' notifications based on current `auth_token`

        :param all: whether to retrieve all notifications, or just new ones
        :type all: bool
        :param participating: whether to show only notifications user is
                              directly participating in
        :type participating: bool
        :param since: optional datetime for start of notification range to fetch
        :type since: Optional[datetime.datetime]
        :param before: optional datetime for end of notification range to fetch
        :type before: Optional[datetime.datetime]
        """
        notifications = self._notifications(
            all=all, participating=participating, since=since, before=before
        )
        start = (page - 1) * per_page
        end = start + per_page
        results = []

        # This avoids making an extra API call to retrieve total count
        try:
            for i in range(start, end):
                n = notifications[i]
                results.append(Notification.load_from_pyghub(n))
        except IndexError:
            pass

        return results

    @lru_cache(maxsize=None)
    def _notifications(
        self,
        all: bool = False,
        participating: bool = False,
        since: Optional[datetime] = None,
        before: Optional[datetime] = None,
    ):
        if since is None:
            since = GithubObject.NotSet
        if before is None:
            before = GithubObject.NotSet

        # Bug with PyGithub
        # If all is present, even if set to
        # False, all results will be returned
        if all == False:
            all = GithubObject.NotSet
        if participating == False:
            participating = GithubObject.NotSet

        return self.github.get_user().get_notifications(
            all=all, participating=participating, since=since, before=before
        )
