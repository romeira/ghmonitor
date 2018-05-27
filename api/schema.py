import graphene

from graphene_django.types import DjangoObjectType

from .models import Repository, Commit


class RepositoryType(DjangoObjectType):

    class Meta:
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
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Repository.objects.get(pk=id)

        if name is not None:
            *owner, name = name.rsplit('/', 1)
            kw = {'name': name}
            if owner:
                kw['owner__username'] = owner[0]
            return Repository.objects.get(**kw)

        return None

    def resolve_repositories(self, info, **kwargs):
        return Repository.objects.all()

    def resolve_commits(self, info, **kwargs):
        return Commit.objects.select_related('repository').all()

