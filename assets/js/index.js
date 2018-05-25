import React from 'react'
import ReactDOM from 'react-dom'
import ApolloClient from "apollo-boost"
import gql from "graphql-tag"

// no django: user.social_auth.get(provider='github')
const AUTH_TOKEN = "";

const client = new ApolloClient({
  uri: "https://api.github.com/graphql",
  request: (operation) => {
    operation.setContext({
      headers: {
        Authorization: "bearer " + AUTH_TOKEN
      },
    });
  },
});


client.query({
    query: gql`
    query {
        user (login: "pauloromeira") {
         repository(name: "onegram") {
           refs(first: 100, refPrefix: "refs/heads/") {
             edges {
               node {
                 name
                 target {
                   ... on Commit {
                     history(since: "2018-05-01T00:00:00") {
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
}).then(result => console.log(result));


ReactDOM.render(<h1>Hello World</h1>, document.getElementById('react-app'));