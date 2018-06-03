from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.serializers import ValidationError

from api.models import Commit, Repository
from api.github import GithubClient


class RepositorySerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Repository
        exclude = ('owner',)

    def validate_name(self, value):
        user = self.context['request'].user
        token = user.social_auth.get(provider='github').access_token
        github = GithubClient(token)
        repo = github.repo_check(value)
        if not repo:
            raise ValidationError('Invalid repository')
        return repo


    def create(self, validated_data):
        return Repository.objects.get_or_create(**validated_data)[0]


class CommitSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Commit
        fields = '__all__'