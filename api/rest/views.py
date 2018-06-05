from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets

from api.github import GithubClient
from api.models import Commit, Repository
from api.tasks import fetch_commits

from .serializers import CommitSerializer, RepositorySerializer


class CommitViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Commit.objects.all()
    serializer_class = CommitSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('repository__name',)

    def get_queryset(self):
        return self.queryset.filter(repository__owner=self.request.user)


class RepositoryViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):

    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def get_serializer_context(self):
        context = super(RepositoryViewSet, self).get_serializer_context()
        user = context['request'].user
        token = user.social_auth.get(provider='github').access_token
        context['github_client'] = GithubClient(token)
        return context

    def perform_create(self, serializer):
        repo = serializer.save(owner=self.request.user)
        github_client = serializer.context['github_client']
        fetch_commits(repo, github_client)
