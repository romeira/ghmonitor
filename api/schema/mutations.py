import graphene
from api.github import GithubClient
from jmespath import search as jsearch


class AddRepository(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    ok = graphene.Boolean()
    repository = graphene.String()

    @staticmethod
    def mutate(root, info, name):
        user = info.context.user
        token = user.social_auth.get(provider='github').access_token
        github = GithubClient(token)
        repo_meta = github.get_repo_meta(name)

        repository = jsearch('viewer.repository.name', repo_meta)
        ok = bool(repository)

        # TODO [romeira]: add repo {27/05/18 23:33}

        return AddRepository(ok=ok, repository=repository)


class Mutation:
    add_repository = AddRepository.Field()
