import graphene
import django_filters

from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from django_filters import FilterSet

from api.models import Commit, Repository


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
                select_related('repository').
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
