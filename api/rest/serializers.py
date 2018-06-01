from rest_framework import serializers

from rest_framework.serializers import HyperlinkedModelSerializer

from api.models import Commit, Repository


class RepositorySerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Repository
        exclude = ('owner',)

    def validate_name(self, value):
        # TODO [romeira]: github.validate_repo {01/06/18 00:28}
        # github = self.context['github_client']
        # return github.validate_repo(value)
        return value

    def create(self, validated_data):
        return Repository.objects.get_or_create(**validated_data)[0]


class CommitSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Commit
        fields = '__all__'
