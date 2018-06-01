from celery import task, group

from api.github import GithubClient
from api.models import Commit, Repository


def fetch_commits(repository, github_client):
    branches = github_client.repo_branches(repository.name)

    job = group(_save_commits.s(repository.id,
                                repository.name,
                                github_client.token,
                                branch,
                                total_commits)
                for branch, total_commits in branches)

    job.delay()


@task
def _save_commits(repo_id, repo_name, github_token, branch_name, total_commits):
    github = GithubClient(github_token)
    commits = github.branch_commits(repo_name, branch_name, total_commits)

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

