from users.models import User

from .github import GithubClient
from .models import Commit, Repository


# TODO [romeira]: celery tasks {28/05/18 12:33}

def add_repository(user_id, github_token, repo_name):
    repository, _ = Repository.objects.update_or_create(
        owner_id=user_id,
        name=repo_name
    )

    github = GithubClient(github_token)
    branches = github.repo_branches(repo_name)

    for branch, total_commits in branches:
        add_commits(repository.id, github_token, repo_name, branch, total_commits)


def add_commits(repository_id, github_token, repo_name, branch_name, total_commits):
    github = GithubClient(github_token)
    commits = github.branch_commits(repo_name, branch_name, total_commits)

    for commit in commits:
        Commit.objects.update_or_create(
            oid=commit['oid'],
            short_oid=commit['abbreviatedOid'],
            message_head=commit['messageHeadline'],
            message=commit['message'],
            date=commit['committedDate'],
            url=commit['commitUrl'],
            committer=commit['committer'],
            repository_id=repository_id,
        )
