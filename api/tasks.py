from jmespath import search as jsearch
from api.models import Commit


# TODO [romeira]: use celery {03/06/18 14:06}
def fetch_commits(repository, github_client):
    branches = github_client.repo_branches(repository.name)

    for branch, commits_count in branches:
        save_commits(repository, github_client, branch, commits_count)


def save_commits(repository, github_client, branch, commits_count):
    commits = github_client.branch_commits(repository.name,
                                           branch, commits_count)

    for commit in commits:
        f = lambda path: jsearch(path, commit)
        Commit.objects.update_or_create(
            oid=commit['oid'],
            repository_id=repository.id,
            defaults={ 
                'short_oid': f('abbreviatedOid'),
                'message_head': f('messageHeadline'),
                'message': f('message'),
                'date': f('committedDate'),
                'url': f('commitUrl'),
                'committer': f('committer.name'),
            }
        )
