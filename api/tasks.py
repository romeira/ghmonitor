from users.models import User
from .models import Repository, Commit
from github import GithubClient


def add_repository(user_id, github_token, repository_name):
    repository, _ = Repository.objects.update_or_create(
        owner_id=user_id,
        name=repository_name
    )

    github = GithubClient(github_token)
    branches = github.repo_branches(repository_name)

    for branch in branches:
        add_commits(repository.id, github_token, branch)


def add_commits(repository_id, github_token, branch_name):
    github = GithubClient(github_token)
    commits = github.branch_commits(repository_name)

    for commit in commits:
        commit['repository_id'] = repository_id
        Commit.objects.update_or_create(**commit)
