from rest_framework import viewsets, mixins

from api.models import Repository, Commit
from api.tasks import fetch_commits
from api.github import GithubClient

from .serializers import RepositorySerializer, CommitSerializer


class CommitViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Commit.objects.all()
    serializer_class = CommitSerializer

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
        result = fetch_commits(repo, github_client)
