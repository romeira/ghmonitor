from rest_framework import serializers

from rest_framework.serializers import HyperlinkedModelSerializer

from api.models import Commit, Repository


class RepositorySerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Repository
        exclude = ('owner',)


class CommitSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Commit
        fields = '__all__'
