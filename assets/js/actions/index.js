import { Urls } from 'utils'

export const REQUEST_COMMITS = 'REQUEST_COMMITS'
export const RECEIVE_COMMITS = 'RECEIVE_COMMITS'
export const SELECT_REPOSITORY = 'SELECT_REPOSITORY'
export const INVALIDATE_REPOSITORY = 'INVALIDATE_REPOSITORY'

export const selectRepository = repository => ({
  type: SELECT_REPOSITORY,
  repository
})

export const invalidateRepository = repository => ({
  type: INVALIDATE_REPOSITORY,
  repository
})

export const requestCommits = repository => ({
  type: REQUEST_COMMITS,
  repository
})

export const receiveCommits = (repository, commits) => {
  return {
    type: RECEIVE_COMMITS,
    repository,
    commits: commits,
    receivedAt: Date.now()
  }
}


export const addRepository = repository => dispatch => {

  const url = Urls['repository-list']()
  const payload = {
    name: repository
  };
  const headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
  }

  const options = {
    method: "POST",
    credentials: 'same-origin',
    headers: headers,
    body: JSON.stringify(payload)
  }

  fetch(url, options)
    .then(response => {
      dispatch(invalidateRepository())
      dispatch(fetchCommitsIfNeeded())
    })
}


const fetchCommits = repository => dispatch => {
  dispatch(requestCommits(repository))

  const options = { credentials: 'same-origin' }
  let url = Urls['commit-list']()
  if (repository) {
    url = `${url}?repository__name=${repository}`
  }

  return fetch(url, options)
    .then(response => response.json())
    .then(commits => dispatch(receiveCommits(repository, commits)))
}

const shouldFetchCommits = (state, repository) => {
  const commits = state.commitsByRepository[repository]
  if (!commits) {
    return true
  }
  if (commits.isFetching) {
    return false
  }
  return commits.didInvalidate
}

export const fetchCommitsIfNeeded = repository => (dispatch, getState) => {
  if (shouldFetchCommits(getState(), repository)) {
    return dispatch(fetchCommits(repository))
  }
}
