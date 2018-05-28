import React from 'react';
import ReactDOM from 'react-dom';
import ApolloClient from 'apollo-boost';
import { createHttpLink } from 'apollo-link-http';
import { ApolloProvider } from "react-apollo";
import { InMemoryCache } from 'apollo-cache-inmemory';
import { GET_COMMITS, ADD_REPO } from '../constants/queries';
import { Query } from "react-apollo";
import { Mutation } from "react-apollo";


const link = createHttpLink({
  uri: 'https://ghmonitor.local.com:8000/graphql',
  credentials: 'same-origin',
});


const client = new ApolloClient({
  cache: new InMemoryCache(),
  link,
});


const AddRepo = () => {
  let input;

  return (
    <Mutation mutation={ADD_REPO}>
      {(addRepo, { data }) => (
        <div>
          <form
            onSubmit={e => {
              e.preventDefault();
              addRepo({ variables: { name: input.value } });
              input.value = "";
            }}
          >
            <input
              ref={node => {
                input = node;
              }}
            />
            <button type="submit">Add Repo</button>
          </form>
        </div>
      )}
    </Mutation>
  );
};


const GetCommits = () => (
  <Query query={GET_COMMITS}>
    {({ loading, error, data }) => {
      if (loading) return <p>Loading...</p>;
      if (error) return <p>Error :(</p>;

      console.log(data);

      return (
        <div>
        {data.commits.map(c => <p key={c.oid}><a href={c.url}>{c.shortOid}</a> [{c.repository.name}] {c.messageHead} </p>)}
        </div>
      );
    }}
  </Query>
);


const App = () => (
  <ApolloProvider client={client}>
    <div>
      <AddRepo></AddRepo>
      <GetCommits></GetCommits>
    </div>
  </ApolloProvider>
);

ReactDOM.render(<App></App>, document.getElementById('react-app'));