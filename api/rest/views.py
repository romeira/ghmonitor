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

    def perform_create(self, serializer):
        repo = serializer.save(owner=self.request.user)

        user = self.request.user
        token = user.social_auth.get(provider='github').access_token

        fetch_commits.delay(repo.id, token)
