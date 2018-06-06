import React from 'react'
import { render } from 'react-dom'
import { createStore, applyMiddleware } from 'redux'
import { Provider } from 'react-redux'
import reducer from './reducers'
import thunk from 'redux-thunk';
import App from './pages/homePage'
import Repo from './pages/repoPage'

import { HashRouter as Router, Route } from 'react-router-dom'



const devTools = window.__REDUX_DEVTOOLS_EXTENSION__
              && window.__REDUX_DEVTOOLS_EXTENSION__()

const store = createStore(
  reducer,
  devTools,
  applyMiddleware(thunk)
);

render((
    <Router>
      <Provider store={store}>
        <div>
          <Route exact path="/" component={App} />
          <Route path="/:repository" component={Repo} />
        </div>
      </Provider>
    </Router>
  ),
  document.getElementById('react-app')
)

