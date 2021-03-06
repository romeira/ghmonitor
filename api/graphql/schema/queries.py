import django_filters
import graphene
from api.models import Commit, Repository
from django_filters import FilterSet
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType


class RepositoryNode(DjangoObjectType):

    class Meta:
        model = Repository
        interfaces = (graphene.Node,)


class RepositoryFilter(FilterSet):

    class Meta:
        model = Repository
        fields = ['name']

    @property
    def qs(self):
        return super(RepositoryFilter, self).qs.filter(owner=self.request.user)


class CommitNode(DjangoObjectType):

    class Meta:
        model = Commit
        interfaces = (graphene.Node,)


class CommitFilter(FilterSet):

    class Meta:
        model = Commit
        fields = ['oid']

    @property
    def qs(self):
        return (super(CommitFilter, self).qs.
                filter(repository__owner=self.request.user))


class Query:

    repositories = DjangoFilterConnectionField(
            RepositoryNode,
            filterset_class=RepositoryFilter
    )

    commits = DjangoFilterConnectionField(
            CommitNode,
            filterset_class=CommitFilter
    )
