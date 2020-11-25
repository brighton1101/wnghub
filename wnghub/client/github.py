from typing import Optional, List
from datetime import datetime
from functools import lru_cache

from github import Github, GithubObject

from wnghub.model.notification import Notification

class BaseGithubClient(object):

    auth_token: str = ''

    def __init__(self, auth_token: str):
        self.auth_token = auth_token

    def get_notifications(
        self,
        all: bool = False,
        participating: bool = False,
        since: Optional[datetime] = None,
        before: Optional[datetime] = None,
        per_page: int = None,
        page: int = 1
    ) -> List[Notification]:
        raise NotImplementedError('Cannot be called directly from base client')


class GithubClient(BaseGithubClient):

    _github = None

    @property
    def github(self):
        if self._github is None:
            self._github = Github(self.auth_token)
        return self._github

    @lru_cache(maxsize = None)
    def get_notifications(
        self,
        all: bool = False,
        participating: bool = False,
        since: Optional[datetime] = None,
        before: Optional[datetime] = None,
        per_page: int = 5,
        page: int = 1
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
            all = all, participating = participating, since = since, before = before)
        start = (page-1)*per_page
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
        before: Optional[datetime] = None
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
            all = all, participating = participating, since = since, before = before)        
