from django.conf import settings
from jmespath import search as jsearch
from gql import Client

from .queries import REPO_CHECK, GET_REPO_META
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


    def repo_branches(self, name):
        # TODO [romeira]: pagination {28/05/18 01:13}
        variables = {
            'repo': name,
            'count': 30
        }
        # TODO [romeira]: REPO_BRANCHES {28/05/18 01:27}
        response = self.execute(REPO_BRANCHES, variables)
        return response


    def repo_check(self, name):
        variables = {'repo': name}
        response = self.execute(REPO_CHECK, variables)
        return jsearch('viewer.repository.name', response)
