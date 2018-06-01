from rest_framework.viewsets import ReadOnlyModelViewSet

from api.models import Commit, Repository

from .serializers import CommitSerializer


class CommitViewSet(ReadOnlyModelViewSet):

    queryset = Commit.objects.select_related('repository')
    serializer_class = CommitSerializer

    def get_queryset(self):
        return self.queryset.filter(repository__owner=self.request.user)
