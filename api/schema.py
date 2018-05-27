import graphene
from graphene_django.types import DjangoObjectType

from .models import Commit, Repository


class RepositoryType(DjangoObjectType):

    class Meta:
        exclude_fields = ('owner',)
        model = Repository


class CommitType(DjangoObjectType):

    class Meta:
        model = Commit


class Query(graphene.AbstractType):
    repository = graphene.Field(RepositoryType, 
                                id=graphene.Int(),
                                name=graphene.String())

    repositories = graphene.List(RepositoryType)
    commits = graphene.List(CommitType)

    def resolve_repository(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            return None

        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Repository.objects.get(pk=id, owner=user)

        if name is not None:
            *owner, name = name.rsplit('/', 1)
            kw = {'name': name, 'owner': user}
            if owner:
                kw['owner__username'] = owner[0]

            return Repository.objects.get(**kw)

        return None

    def resolve_repositories(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            return Repository.objects.none()

        return Repository.objects.filter(owner=user)

    def resolve_commits(self, info, **kwargs):
        user = info.context.user
        if not user.is_authenticated:
            return Commit.objects.none()

        return Commit.objects.select_related('repository').filter(
                   repository__owner=user
               )
