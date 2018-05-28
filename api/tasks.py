from users.models import User
from .models import Repository, Commit
from github import GithubClient


def add_repository(user_id, github_token, repo_name):
    repository, _ = Repository.objects.update_or_create(
        owner_id=user_id,
        name=repo_name
    )

    github = GithubClient(github_token)
    branches = github.repo_branches(repo_name)

    for branch, total_commits in branches:
        add_commits(repository.id, github_token, branch, total_commits)


def add_commits(repository_id, github_token, repo_name, branch_name, total_commits):
    github = GithubClient(github_token)
    commits = github.branch_commits(repo_name, branch_name, total_commits)

    for commit in commits:
        commit['repository_id'] = repository_id
        Commit.objects.update_or_create(**commit)
