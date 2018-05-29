import graphene
from api.github import GithubClient
from api.tasks import add_repository


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
        # TODO [romeira]: improve {29/05/18 00:48}
        name = name.rsplit('/', 1)[-1]
        repository = github.repo_check(name)
        ok = bool(repository)

        if ok: add_repository(user.id, token, repository)

        return AddRepository(ok=ok, repository=repository)


class Mutation:
    add_repository = AddRepository.Field()
