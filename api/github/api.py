from django.conf import settings

from gql import Client
from .transport import RequestsTransport

from .queries import GET_REPO_META


class GithubApi:

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
        # proxies = {
        #     'http': 'http://127.0.0.1:8080',
        #     'https': 'https://127.0.0.1:8080',
        # }
        # return self._client.execute(query, variables, proxies=proxies, verify=False)
        return self._client.execute(query, variables)


    def get_repo_meta(self, name):
        variables = {
            'repo': name,
            'count': 30
        }
        response = self.execute(GET_REPO_META, variables)
        return response
