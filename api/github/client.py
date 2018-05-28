from django.conf import settings
from jmespath import search as jsearch
from gql import Client

from .queries import REPO_CHECK, REPO_BRANCHES
from .queries import BRANCH_COMMITS
from .transport import RequestsTransport


class GithubClient:

    def __init__(self, token, endpoint=None):
        transport = RequestsTransport(
            endpoint=endpoint or settings.GITHUB_ENDPOINT,
            use_json=True,
        )
        transport.session.headers['Authorization'] = f'bearer {token}'

        # TODO [romeira]: remove proxy {27/05/18 22:53}
        transport.session.verify = False
        transport.session.proxies =  {
            'http': 'http://127.0.0.1:8080',
            'https': 'https://127.0.0.1:8080',
        }

        self._client = Client(
            retries=3,
            transport=transport,
            introspection=False
        )


    def execute(self, query, variables={}):
        return self._client.execute(query, variables)


    def repo_check(self, name):
        variables = {'repo': name}
        response = self.execute(REPO_CHECK, variables)
        # TODO [romeira]: move to constants {28/05/18 10:41}
        return jsearch('viewer.repository.name', response)


    def repo_branches(self, repo):
        variables = {
            'repo': repo,
            'count': 30,
            # 'since': TODO
        }
        # TODO [romeira]: move to constants {28/05/18 10:40}
        branches_path = 'viewer.repository.refs.nodes[?target.history.totalCount > `0`].[name, target.history.totalCount]'
        pages_path = 'viewer.repository.refs.pageInfo'
        pages = self.pagination(pages_path, REPO_BRANCHES, variables)
        for page in pages:
            branches = jsearch(branches_path, page)
            if branches:
                yield from branches


    def branch_commits(self, repo, branch, total_commits=None):
        count = min(total_commits, 100) if total_commits else 30
        variables = {
            'repo': repo,
            'branch': branch,
            'count': count,
            # 'since': TODO
        }
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


