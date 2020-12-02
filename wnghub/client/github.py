from typing import Optional, List
from datetime import datetime
from functools import lru_cache
from requests import request
from abc import ABC, abstractmethod

from wnghub.model.notification import Notification


class BaseGithubClient(ABC):
    """
    Base Github client class for interacting with
    Github. This allows for multiple different implementations
    for interacting with Github (ie, `PyGithub`, raw HTTP calls,
    GraphQL, etc.)
    """

    auth_token: str = ""

    def __init__(self, auth_token: str):
        if auth_token is None or auth_token == "":
            raise BadCredentialsError(
                "Missing auth token. Please set valid auth token and try again."
            )
        self.auth_token = auth_token

    @abstractmethod
    def get_notifications(
        self,
        all: bool = False,
        participating: bool = False,
        since: Optional[datetime] = None,
        before: Optional[datetime] = None,
        per_page: int = None,
        page: int = 1,
    ) -> List[Notification]:
        pass

    @abstractmethod
    def update_notification_status(
        self,
        notification: Notification,
        read: bool = True,
    ):
        pass


class GithubApiClient(BaseGithubClient):
    """
    Implementation of `BaseGithubClient` using raw HTTP calls
    to Github's API.

    :param auth_token: Github personal access token
    :type auth_token: str
    """

    _notifications_url = "https://api.github.com/notifications"

    _notifications_status_url = "https://api.github.com/notifications/threads"

    _unauthorized_code = 401

    _auth_token_info_url = "https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token"  # noqa

    @property
    def default_headers(self):
        """
        The default headers for hitting Github endpoints.
        """
        return {
            "Authorization": "token {}".format(self.auth_token),
            "accept": "application/vnd.github.v3+json",
        }

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
        :return: List[Notification]
        """
        raw_res = self._notifications(
            all=all,
            participating=participating,
            since=since,
            before=before,
            per_page=per_page,
            page=page,
        )
        res = Notification.load_from_json_str(raw_res)
        return res

    def update_notification_status(
        self,
        notification: Notification,
        read: bool = True,
    ):
        """
        Updates notification status for given notification.

        Currently does not support marking notification as
        unread - when `read = False`

        :param notification: notification to update
        :type notification: Notification
        :param read: whether or not to mark thread as read
        :type read: bool
        """
        if not read:
            raise NotImplementedError(
                "Github client currently does not "
                "support marking notification as "
                "unread."
            )
        thread_id = notification.thread_id
        if thread_id is None or thread_id == "":
            raise GithubHttpException("Thread ID missing from given " "Notification.")
        url = "{}/{}".format(self._notifications_status_url, notification.thread_id)
        headers = self.default_headers
        res = request("PATCH", url, headers=headers)
        status_code = res.status_code
        self._unauthorized_status_code(status_code)
        if not (status_code == 205 or status_code == 304):
            raise GithubHttpException("Unknown error with Github API.")

    @lru_cache(maxsize=None)
    def _notifications(
        self,
        all: bool = False,
        participating: bool = False,
        since: Optional[datetime] = None,
        before: Optional[datetime] = None,
        page: int = 1,
        per_page: int = 10,
    ) -> str:
        """
        API call for getting notifications

        :param all: whether to retrieve all notifications, or just new ones
        :type all: bool
        :param participating: whether to show only notifications user is
                              directly participating in
        :type participating: bool
        :param since: optional datetime for start of notification range to fetch
        :type since: Optional[datetime.datetime]
        :param before: optional datetime for end of notification range to fetch
        :type before: Optional[datetime.datetime]
        :return: str
        """
        headers = self.default_headers
        params = {
            "all": "true" if all else "false",
            "participating": "true" if participating else "false",
            "page": page,
            "per_page": per_page,
        }
        if since is not None:
            params["since"] = since.isoformat()
        if before is not None:
            params["before"] = before.isoformat()
        if per_page > 100:
            raise Exception(
                "Github API support maximum 100 notifications per page for api calls"
            )
        res = request("GET", self._notifications_url, headers=headers, params=params)
        status_code = res.status_code
        self._unauthorized_status_code(status_code)
        if status_code != 200:
            raise GithubHttpException("Unknown error occurred with Github API.")
        return res.text

    def _unauthorized_status_code(self, code):
        """
        Checks if code is the given unauthorized status code.

        :raises BadCredentialsError: if token is invalid.
        """
        if code == self._unauthorized_code:
            raise BadCredentialsError(
                "Invalid auth token supplied. Please "
                "ensure valid Github personal auth token "
                "is present. See {} for more info".format(self._auth_token_info_url)
            )


class BadCredentialsError(Exception):
    pass


class GithubHttpException(Exception):
    pass
