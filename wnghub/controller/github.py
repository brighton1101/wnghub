from wnghub.controller.base import BaseController
from wnghub.config.config import Config
from wnghub.client.github import BaseGithubClient
from wnghub.model.filter import AggregateFilter
from wnghub.model.notification import Notification, NotificationReposFilter, NotificationReasonsFilter, NotificationPrIssuesFilter, NotificationOrgsFilter
from datetime import datetime, timedelta


class GithubController(BaseController):
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
