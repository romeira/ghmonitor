from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from api.models import Commit, Repository

from .serializers import CommitSerializer


class CommitViewSet(ReadOnlyModelViewSet):

    queryset = Commit.objects.all()
    serializer_class = CommitSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(repository__owner=self.request.user)
