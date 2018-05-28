from graphql.execution import ExecutionResult
from graphql.language.printer import print_ast
from requests import Session


class RequestsTransport():

    def __init__(self, endpoint, use_json=False):
        self.endpoint = endpoint
        self.session = Session()
        self.use_json = True


    def execute(self, query, variables={}, **kwargs):
        payload = {
            'query': print_ast(query),
            'variables': variables
        }
        payload_key = 'json' if self.use_json else 'data'
        kwargs[payload_key] = payload

        response = self.session.post(self.endpoint, **kwargs)
        response.raise_for_status()

        result = response.json()
        assert ('errors' in result or 'data' in result), f'Received non-compatible response "{result}"'

        return ExecutionResult(
            errors=result.get('errors'),
            data=result.get('data')
        )


    def __del__(self):
        try:
            self.session.close()
        except:
            pass
