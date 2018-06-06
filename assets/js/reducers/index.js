import { combineReducers } from 'redux'
import {
  SELECT_REPOSITORY, INVALIDATE_REPOSITORY,
  REQUEST_COMMITS, RECEIVE_COMMITS
} from '../actions'

const selectedRepository = (state = '', action) => {
  switch (action.type) {
    case SELECT_REPOSITORY:
      return action.repository
    default:
      return state
  }
}

const commits = (state = {
  isFetching: false,
  didInvalidate: false,
  items: []
}, action) => {
  switch (action.type) {
    case INVALIDATE_REPOSITORY:
      return Object.assign({}, state, {
        didInvalidate: true
      })
    case REQUEST_COMMITS:
      return Object.assign({}, state, {
        isFetching: true,
        didInvalidate: false
      })
    case RECEIVE_COMMITS:
      return Object.assign({}, state, {
        isFetching: false,
        didInvalidate: false,
        items: action.commits,
        lastUpdated: action.receivedAt
      })
    default:
      return state
  }
}

const commitsByRepository = (state = { }, action) => {
  switch (action.type) {
    case INVALIDATE_REPOSITORY:
    case RECEIVE_COMMITS:
    case REQUEST_COMMITS:
      return Object.assign({}, state, {
        [action.repository]: commits(state[action.repository], action)
      })
    default:
      return state
  }
}

const rootReducer = combineReducers({
  commitsByRepository,
  selectedRepository
})

export default rootReducer
