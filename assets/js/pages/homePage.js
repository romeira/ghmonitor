import React from 'react';
import ReactDOM from 'react-dom';
import ApolloClient from 'apollo-boost';
import { createHttpLink } from 'apollo-link-http';
import { ApolloProvider } from "react-apollo";
import { InMemoryCache } from 'apollo-cache-inmemory';
import { GET_COMMITS } from '../constants/queries';
import { Query } from "react-apollo";


const link = createHttpLink({
  uri: 'https://ghmonitor.local.com:8000/graphql',
  credentials: 'same-origin',
});


const client = new ApolloClient({
  cache: new InMemoryCache(),
  link,
});


const GetCommits = () => (
  <Query query={GET_COMMITS}>
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
      <GetCommits></GetCommits>
    </div>
  </ApolloProvider>
);

ReactDOM.render(<App></App>, document.getElementById('react-app'));