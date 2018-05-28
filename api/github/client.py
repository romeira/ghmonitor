from django.conf import settings

from gql import Client
from jmespath import search as jsearch

from .queries import REPO_BRANCHES, REPO_CHECK
from .transport import RequestsTransport


class GithubClient:

    def __init__(self, token, endpoint=None):
        transport = RequestsTransport(
            endpoint=endpoint or settings.GITHUB_ENDPOINT,
            use_json=True,
        )
        transport.session.headers['Authorization'] = f'bearer {token}'
        self._client = Client(
            retries=3,
            transport=transport,
            fetch_schema_from_transport=True,
        )


    def execute(self, query, variables={}):
        # TODO [romeira]: remove proxy {27/05/18 22:53}
        proxies = {
            'http': 'http://127.0.0.1:8080',
            'https': 'https://127.0.0.1:8080',
        }
        return self._client.execute(query, variables, proxies=proxies, verify=False)
        # return self._client.execute(query, variables)


    def repo_check(self, name):
        variables = {'repo': name}
        response = self.execute(REPO_CHECK, variables)
        # TODO [romeira]: move to constants {28/05/18 10:41}
        return jsearch('viewer.repository.name', response)


    def repo_branches(self, name):
        variables = {
            'repo': name,
            'count': 30,
            # 'since': 
        }
        # TODO [romeira]: move to constants {28/05/18 10:40}
        branches_path = 'viewer.repository.refs.nodes[?target.history.totalCount > `0`].name'
        pages_path = 'viewer.repository.refs.pageInfo'
        pages = self.pagination(pages_path, REPO_BRANCHES, variables)
        for page in pages:
            branches = jsearch(branches_path, page)
            if branches:
                yield from branches


    def pagination(self, pages_path, query, variables={}):
        response = self.execute(query, variables)
        yield response
        pages = jsearch(pages_path, response)
        while pages and pages.get('hasNextPage', False):
            variables['cursor'] = pages['endCursor']
            response = self.execute(query, variables)
            yield response
            pages = jsearch(pages_path, response)
