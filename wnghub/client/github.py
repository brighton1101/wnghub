from typing import Optional
from datetime import datetime
from functools import cached_property

from github import Github

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
    ):
        raise NotImplementedError('Cannot be called directly from client')


class GithubClient(BaseGithubClient):

    @cached_property
    def _github(self):
        return Github(self.auth_token)

    def get_notifications(
        self,
        all: bool = False,
        participating: bool = False,
        since: Optional[datetime] = None,
        before: Optional[datetime] = None,
        per_page: int = None,
        page: int = 1
    ):
        pass
        