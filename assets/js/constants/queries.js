import gql from "graphql-tag"


export const GET_COMMITS = gql`
{
  commits {
    messageHead
    date
  }
}`
