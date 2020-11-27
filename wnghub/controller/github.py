from wnghub.controller.base import BaseController
from wnghub.config.config import Config
from wnghub.client.github import BaseGithubClient
from wnghub.model.filter import AggregateFilter
from wnghub.model.notification import Notification, NotificationReposFilter, NotificationReasonsFilter, NotificationPrIssuesFilter, NotificationOrgsFilter
from datetime import datetime, timedelta


class GithubController(BaseController):
    """
    Class for managing user interaction with Github functionality.

    :param client: The client to use to interact with Github's API
    :type client: Subclass of `BaseGithubClient`
    :param config: the application config to use
    :type config: Config
    """
    def __init__(self, client: BaseGithubClient, config: Config):
        self.client = client
        BaseController.__init__(self, config)

    def get_notifications(
        self,
        num_results=5,
        include_repos=None,
        include_orgs=None,
        include_reasons=None,
        exclude_repos=None,
        exclude_orgs=None,
        exclude_reasons=None,
        all=False,
        participating=False,
        since=None,
        before=None,
        show_issues=True,
        show_prs=True,
    ):
        """
        Method to get notifications for user.

        TODO: Add capability to set defaults in config for these values, and then
        reconcile below with priority first given to set kwargs, then to config values,
        then to defaults.

        :param num_results: number of results to fetch, after applying filters (default 5)
        :type num_results: int
        :param include_repos: only include these repos in res (optional)
        :type include_repos: List[str]
        :param include_reasons: only include these reasons in res (optional)
        :type include_reasons: List[str]
        :param include_orgs: only include these orgs in res (optional)
        :type include_orgs: List[str]
        :param exclude_repos: exclude these repos in res (optional)
        :type exclude_repos: List[str]
        :param exclude_orgs: exclude these orgs in res (optional)
        :type exclude_orgs: List[str]
        :param exclude_reasons: exclude these reasons in res (optional)
        :type exclude_reasons: List[str]
        :param all: Get both read/unread notifications (default False)
        :type all: bool
        :param participating: Only notifications user is participating in (default false)
        :type participating: bool
        :param since: starting date to fetch notifications for (default None)
        :type since: datetime
        :param before: ending date to fetch notifications for (default None)
        :type before: datetime
        :param show_issues: whether to show issues or not (default True)
        :type show_issues: bool
        :param show_prs: whether to show prs or not (default True)
        :type show_prs: bool
        """
        n_filters = []
        if include_repos is not None:
            n_filters.append(NotificationReposFilter(include_repos))
        if exclude_repos is not None:
            n_filters.append(NotificationReposFilter(exclude_repos, exlcude=True))
        if include_orgs is not None:
            n_filters.append(NotificationOrgsFilter(include_orgs))
        if exclude_orgs is not None:
            n_filters.append(NotificationOrgsFilter(exclude_orgs, exlcude=True))
        if include_reasons is not None:
            n_filters.append(NotificationReasonsFilter(include_reasons))
        if exclude_reasons is not None:
            n_filters.append(NotificationReasonsFilter(exclude_reasons), exclude=True)
        n_filters.append(NotificationPrIssuesFilter(get_prs=show_prs, get_issues=show_issues))
        filters = AggregateFilter(n_filters)
        res = []
        page = 1
        per_page = 100 # TODO: maybe add this to config?
        while len(res) < num_results:
            pre_filtered_results = self.client.get_notifications(all=all, participating=participating, since=since, before=before, page=page, per_page=per_page)
            filtered_results = filters.apply(pre_filtered_results)
            if len(filtered_results) > num_results:
                filtered_results = filtered_results[0:num_results]
                num_results = 0
            else:
                num_results = num_results - len(filtered_results)
            res.extend(filtered_results)
            if len(pre_filtered_results) < per_page:
                break
            if num_results <= 0:
                break
            page += 1
        return res
