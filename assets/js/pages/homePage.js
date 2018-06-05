import React from 'react';
import ReactDOM from 'react-dom';
import { CommitList, AddRepository } from 'components'


const App = () => (
  <div>
    <h1>Github Monitor</h1>
    <AddRepository />
    <CommitList />
  </div>
);

ReactDOM.render(<App />, document.getElementById('react-app'))