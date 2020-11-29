from wnghub.controller.base import BaseController
from wnghub.config.config import Config
from wnghub.client.github import BaseGithubClient
from wnghub.model.filter import AggregateFilter
from wnghub.model.notification import (
    NotificationReposFilter,
    NotificationReasonsFilter,
    NotificationPrIssuesFilter,
    NotificationOrgsFilter,
)
from wnghub.util.kwargs import Kwarg, KwargsReconciler


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

    @property
    def notifications_kwargs(self):
        """
        `KwargsReconciler` configured with default kwargs
        for `get_notifications` with injected config.
        :type: `KwargsReconciler`
        """
        return KwargsReconciler(
            Kwarg("num_results", "show_num_results", 5),
            Kwarg("include_repos", "only_include_repos", None),
            Kwarg("include_orgs", "only_include_orgs", None),
            Kwarg("include_reasons", "only_include_reasons", None),
            Kwarg("exclude_repos", "exclude_repos", None),
            Kwarg("exclude_orgs", "exclude_orgs", None),
            Kwarg("exclude_reasons", "exclude_reasons", None),
            Kwarg("all", "show_read_results", False),
            Kwarg("participating", "only_include_participating", False),
            Kwarg("since", "only_include_since", None),
            Kwarg("before", "only_include_before", None),
            Kwarg("show_issues", "include_issues", True),
            Kwarg("show_prs", "include_prs", True),
            config=self.config,
        )

    def get_notifications(self, **kwargs):
        """
        Method to get notifications for user.

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

        def rarg(arg_name):
            return kwargs.get(arg_name) or self.notifications_kwargs.reconcile(arg_name)

        num_results = rarg("num_results")
        include_repos = rarg("include_repos")
        include_orgs = rarg("include_orgs")
        include_reasons = rarg("include_reasons")
        exclude_repos = rarg("exclude_repos")
        exclude_orgs = rarg("exclude_orgs")
        exclude_reasons = rarg("exclude_reasons")
        all = rarg("all")
        participating = rarg("participating")
        since = rarg("since")
        before = rarg("before")
        show_issues = rarg("show_issues")
        show_prs = rarg("show_prs")
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
        n_filters.append(
            NotificationPrIssuesFilter(get_prs=show_prs, get_issues=show_issues)
        )
        filters = AggregateFilter(n_filters)
        res = []
        page = 1
        per_page = 100  # TODO: maybe add this to config?
        while len(res) < num_results:
            pre_filtered_results = self.client.get_notifications(
                all=all,
                participating=participating,
                since=since,
                before=before,
                page=page,
                per_page=per_page,
            )
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
