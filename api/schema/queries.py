import graphene
from graphene_django.types import DjangoObjectType

from api.models import Commit, Repository


class RepositoryType(DjangoObjectType):

    class Meta:
        model = Repository


class CommitType(DjangoObjectType):

    class Meta:
        model = Commit


class Query:
    repository = graphene.Field(RepositoryType, 
                                id=graphene.Int(),
                                name=graphene.String())

    repositories = graphene.List(RepositoryType)
    commits = graphene.List(CommitType)

    def resolve_repository(self, info, **kwargs):
        user = info.context.user

        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Repository.objects.get(pk=id, owner=user)

        if name is not None:
            *owner, name = name.rsplit('/', 1)
            if owner and owner[-1] != user.username:
                return None

            return Repository.objects.get(name=name, owner=user)

        return None

    def resolve_repositories(self, info, **kwargs):
        return Repository.objects.filter(owner=info.context.user)

    def resolve_commits(self, info, **kwargs):
        return Commit.objects.select_related('repository').filter(
                   repository__owner=info.context.user
               )
