from wnghub.controller.base import BaseController
from wnghub.config.config import Config
from wnghub.client.github import GithubClient
from datetime import datetime, timedelta


class GithubController(BaseController):

    def __init__(self, client: GithubClient, config: Config):
        self.client = client
        BaseController.__init__(self, config)

    def get_notifications(
        self,
        num_results = 5,
        valid_repos = None,
        valid_orgs = None,
        valid_reasons = None,
        all = False,
        participating = False,
        since = datetime.now() - timedelta(days = 5),
        before = datetime.now(),
        show_issues = True,
        show_prs = True
    ):
        pass

