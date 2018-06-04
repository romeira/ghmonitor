import React from 'react';
import ReactDOM from 'react-dom';
import { CommitList, RepositoryForm } from 'components'


const App = () => (
  <div>
    <h1>Github Monitor</h1>
    <RepositoryForm />
    <CommitList />
  </div>
);

ReactDOM.render(<App />, document.getElementById('react-app'))