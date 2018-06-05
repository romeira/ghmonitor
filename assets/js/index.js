import React from 'react'
import { render } from 'react-dom'
import { createStore, applyMiddleware } from 'redux'
import { Provider } from 'react-redux'
import reducer from './reducers'
import App from './pages/homePage'
import thunk from 'redux-thunk';


const store = createStore(
  reducer,
  applyMiddleware(thunk)
);

render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('react-app')
)