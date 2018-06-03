import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { CommitList } from 'components'


const App = () => (
  <div>
    <h1>Github Monitor</h1>
    <CommitList />
  </div>
);

ReactDOM.render(<App></App>, document.getElementById('react-app'));
