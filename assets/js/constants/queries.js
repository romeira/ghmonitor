import gql from "graphql-tag"


export const GET_COMMITS = gql`
{
  commits {
    edges {
      node {
        oid
        shortOid
        messageHead
        date
        url
        repository{
          name
        }
      }
    }
  }
}
`


export const ADD_REPO = gql`
mutation addRepo($name: String!) {
  addRepository(name: $name) {
    ok
    repository
  }
}
`;
