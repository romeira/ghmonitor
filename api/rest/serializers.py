from rest_framework.serializers import ModelSerializer

from api.models import Commit, Repository


class CommitSerializer(ModelSerializer):
    class Meta:
        model = Commit
        fields = '__all__'
