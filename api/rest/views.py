from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.models import Repository, Commit

from .serializers import RepositorySerializer, CommitSerializer


class CommitViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Commit.objects.all()
    serializer_class = CommitSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(repository__owner=self.request.user)


class RepositoryViewSet(viewsets.ModelViewSet):

    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
