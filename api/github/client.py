from datetime import datetime, timedelta

from django.conf import settings

from gql import Client
from jmespath import search as jsearch

from .queries import BRANCH_COMMITS, REPO_BRANCHES, REPO_CHECK
from .transport import RequestsTransport


class GithubClient:

    def __init__(self, token, endpoint=None):
        transport = RequestsTransport(
            endpoint=endpoint or settings.GITHUB_ENDPOINT,
            use_json=True,
        )
        self.token = token
        transport.session.headers['Authorization'] = f'bearer {token}'
        self._since = datetime.now() - timedelta(days=30)

        self._client = Client(
            retries=3,
            transport=transport,
            introspection=False
        )


    def execute(self, query, variables={}):
        return self._client.execute(query, variables)


    def repo_check(self, name):
        *login, repo = name.split('/')
        if len(login) > 1:
            return None

        variables = {'repo': repo}
        response = self.execute(REPO_CHECK, variables)

        if login and login[0] != jsearch('viewer.login', response):
            return None

        return jsearch('viewer.repository.name', response)


    def repo_branches(self, repo):
        variables = {
            'repo': repo,
            'count': 30,
            'since': self._since.isoformat()
        }
        # TODO [romeira]: move to constants {28/05/18 10:40}
        branches_path = ('viewer.repository.refs.nodes'
                         '[?target.history.totalCount > `0`].'
                         '[name, target.history.totalCount]')
        pages_path = 'viewer.repository.refs.pageInfo'
        pages = self.pagination(pages_path, REPO_BRANCHES, variables)
        for page in pages:
            branches = jsearch(branches_path, page)
            if branches:
                yield from branches


    def branch_commits(self, repo, branch, commits_count=None):
        count = min(commits_count, 100) if commits_count else 30
        variables = {
            'repo': repo,
            'branch': branch,
            'count': count,
            'since': self._since.isoformat()
        }
        # TODO [romeira]: move to constants {28/05/18 10:40}
        commits_path = 'viewer.repository.ref.target.history.nodes'
        pages_path = 'viewer.repository.ref.target.history.pageInfo'
        pages = self.pagination(pages_path, BRANCH_COMMITS, variables)
        for page in pages:
            commits = jsearch(commits_path, page)
            if commits:
                yield from commits


    def pagination(self, pages_path, query, variables={}):
        response = self.execute(query, variables)
        yield response
        pages = jsearch(pages_path, response)
        while pages and pages.get('hasNextPage', False):
            variables['cursor'] = pages['endCursor']
            response = self.execute(query, variables)
            yield response
            pages = jsearch(pages_path, response)
