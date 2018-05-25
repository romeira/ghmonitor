import React from 'react'
import ReactDOM from 'react-dom'
import ApolloClient from 'apollo-boost'
import { Query } from "react-apollo";
import { ApolloProvider } from "react-apollo";
import { GET_BRANCHES } from './constants/queries'


// no django: user.social_auth.get(provider='github')
const AUTH_TOKEN = "";

const client = new ApolloClient({
  uri: "https://api.github.com/graphql",
  request: (operation) => {
    operation.setContext({
      headers: { Authorization: "bearer " + AUTH_TOKEN },
    });
  },
});


const GetBranches = () => (
  <Query query={GET_BRANCHES}
    variables={{
      repo: "ghmonitor",
      since: "2018-05-01T00:00:00"
    }}
  >
    {({ loading, error, data }) => {
      if (loading) return <p>Loading...</p>;
      if (error) return <p>Error :(</p>;

      console.log(data);

      return (
        <p>test</p>
      );
    }}
  </Query>
);


const App = () => (
  <ApolloProvider client={client}>
    <div>
      <h2>My first Apollo app 🚀</h2>
      <GetBranches></GetBranches>
    </div>
  </ApolloProvider>
);

ReactDOM.render(<App></App>, document.getElementById('react-app'));
