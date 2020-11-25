from wnghub.controller.base import BaseController
from wnghub.config.config import Config
from github import Github
from github.GithubException import BadCredentialsException
from datetime import datetime, timedelta

class GithubController(BaseController):

    github: Optional[Github] = None

    def __init__(self, config: Config):
        self.config = config
        self._init_github()

    def get_notifications(
        self,
        num_results = 5,
        valid_repos = None,
        valid_reasons = None,
        all = False,
        participating = False,
        since = datetime.now() - timedelta(days = 5),
        before = datetime.now(),
        show_issues = True,
        show_prs = True
    ):
        results = []
        notifications = self._get_notifications(
            all=all, participating=participating, since=since, before=before)
        for n in notifications:
            if num_results < 1:
                break
            elif valid_reasons is not None and n.reason is not in valid_reasons:
                continue
            elif valid_repos is not None and n.repository is not in valid_repos:
                continue
            elif not show_issues or not show_prs:
                is_pr = self._pr_or_issue(n)
                if is_pr and not show_prs:
                    continue
                elif not is_pr and not show_issues:
                    continue
            results.append(n)
            num_results -=1
        return results

    def _pr_or_issue(self, notification):
        """
        Differentiate between pr and issue

        :return: True if PR, False if issue
        """
        return notification.get_pull_request().diff_url == None

    def _get_notifications(**kwargs):
        return self.github.get_user().get_notifications(**kwargs)

    def set_auth(
        self,
        auth_token: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None
    ) -> bool:
        self.config.set_credentials(
            auth_token=auth_token, username=username, password=password)
        self._init_github()
        return valid_auth()

    def valid_auth(self) -> bool:
        try:
            self.github.get_user().get_notifications().totalCount
        except BadCredentialsException:
            return False
        return True

    def _init_github(self):
        creds = self._get_credentials()
        self.github = Github(*creds)

    def _get_credentials(self):
        at, user_pw = self.config.get_credentials()
        if at is None:
            return user_pw
        else:
            return at,

