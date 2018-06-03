import graphene

from api.github import GithubClient
from api.models import Repository
from api.tasks import fetch_commits


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
        name = github.repo_check(name)
        ok = bool(name)

        if ok:
            repo, _ = Repository.objects.get_or_create(owner=user, name=name)
            fetch_commits(repo, github)

        return AddRepository(ok=ok, repository=repo)


class Mutation:
    add_repository = AddRepository.Field()
