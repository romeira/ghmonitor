from celery import task, group

from api.github import GithubClient
from api.models import Commit, Repository


@task
def fetch_commits(repo_id, github_token):
    repo = Repository.objects.get(id=repo_id)
    github = GithubClient(github_token)
    branches = github.repo_branches(repo.name)

    for branch, commits_count in branches:
        _save_commits.delay(
            repo.id,
            repo.name,
            github_token,
            branch,
            commits_count
        )

    return repo.name


@task
def _save_commits(repo_id, repo_name, github_token, branch_name, commits_count):
    github = GithubClient(github_token)
    commits = github.branch_commits(repo_name, branch_name, commits_count)

    for commit in commits:
        # TODO [romeira]: use jmespath to get fields to
        # avoid keyerror exceptions {31/05/18 22:19}
        Commit.objects.update_or_create(
            oid=commit['oid'],
            repository_id=repo_id,
            defaults={ 
                'short_oid': commit['abbreviatedOid'],
                'message_head': commit['messageHeadline'],
                'message': commit['message'],
                'date': commit['committedDate'],
                'url': commit['commitUrl'],
                'committer': commit['committer'].get('name'),
            }
        )

    return repo_name, branch_name
