import gql from "graphql-tag"


export const GET_BRANCHES = gql`
query ($repo: String!, $count: Int!, $since: GitTimestamp) {
  viewer {
    repository(name: $repo) {
      refs(first: $count, refPrefix: "refs/heads/") {
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
` 

export const GET_COMMITS = gql`
query ($repo: String!, $branch: String!, $count: Int!, $since: GitTimestamp) {
  viewer {
    repository(name: $repo) {
      ref(qualifiedName: $branch){
        target {
          ... on Commit {
            history(first: $count, since: $since) {
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
`