import gql from "graphql-tag"


export const GET_BRANCHES = gql`
query ($repo: String!, $since: GitTimestamp) {
  viewer {
    repository(name: $repo) {
      refs(first: 100, refPrefix: "refs/heads/") {
        edges {
          node {
            name
            target {
              ... on Commit {
                history(since: $since) {
                  totalCount
                }
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