from gql import gql


REPO_CHECK = gql('''
query ($repo: String!) {
  viewer{
    repository(name: $repo) {
      name
    }
  }
}
''')

REPO_BRANCHES = gql('''
query ($repo: String!, $count: Int!, $cursor: String, $since: GitTimestamp) {
  viewer{
    repository(name: $repo) {
      refs(first: $count, refPrefix: "refs/heads/", after: $cursor) {
        nodes {
          name
          target {
            ... on Commit {
              history(since: $since) {
                totalCount
              }
            }
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
      }
    }
  }
}
''')

GET_COMMITS = gql('''
query ($repo: String!, $branch: String!, $count: Int!, $cursor: String, $since: GitTimestamp) {
  viewer {
    repository(name: $repo) {
      ref(qualifiedName: $branch){
        target {
          ... on Commit {
            history(first: $count, since: $since, after: $cursor) {
              totalCount
              nodes {
                id
                abbreviatedOid
                messageHeadline
                authoredDate
                commitUrl
                committer {
                  name
                }
              }
              pageInfo {
                endCursor
                hasNextPage
              }
            }
          }
        }
      }
    }
  }
}
''')
