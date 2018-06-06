import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { selectRepository,
         fetchCommitsIfNeeded,
         invalidateRepository,
         addRepository
} from '../actions'
import { CommitList, AddRepository } from '../components'


class App extends Component {
  constructor(...args){
    super(...args)

    this.handleAdd = this.handleAdd.bind(this)
    this.handleChange = this.handleChange.bind(this)
    this.handleRefreshClick = this.handleRefreshClick.bind(this)
  }

  componentDidMount() {
    const { dispatch, repository } = this.props
    dispatch(fetchCommitsIfNeeded(repository))
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.repository !== this.props.repository) {
      const { dispatch, repository } = nextProps
      dispatch(fetchCommitsIfNeeded(repository))
    }
  }

  handleChange(nextRepository) {
    this.props.dispatch(selectRepository(nextRepository))
  }

  handleAdd(repository) {
    this.props.dispatch(addRepository(repository))
  }

  handleRefreshClick(e){
    e.preventDefault()

    const { dispatch, repository } = this.props
    dispatch(invalidateRepository(repository))
    dispatch(fetchCommitsIfNeeded(repository))
  }

  render() {
    const { commits, isFetching, lastUpdated } = this.props
    const isEmpty = commits.length === 0
    return (
      <div>
        <AddRepository onSubmit={this.handleAdd} />
        <p>
          {lastUpdated &&
            <span>
              Last updated at {new Date(lastUpdated).toLocaleTimeString()}.
              {' '}
            </span>
          }
          {!isFetching &&
            <button onClick={this.handleRefreshClick}>
              Refresh
            </button>
          }
        </p>
        {isEmpty
          ? (isFetching ? <h2>Loading...</h2> : <h2>Empty.</h2>)
          : <div style={{ opacity: isFetching ? 0.5 : 1 }}>
              <CommitList commits={commits} />
            </div>
        }
      </div>
    )
  }
}

App.propTypes = {
  repository: PropTypes.string,
  commits: PropTypes.array.isRequired,
  isFetching: PropTypes.bool.isRequired,
  lastUpdated: PropTypes.number,
  dispatch: PropTypes.func.isRequired
}

const mapStateToProps = state => {
  const { repository, commitsByRepository } = state
  const {
    isFetching,
    lastUpdated,
    items: commits
  } = commitsByRepository[repository] || {
    isFetching: true,
    items: []
  }

  return {
    repository,
    commits,
    isFetching,
    lastUpdated
  }
}

export default connect(mapStateToProps)(App)
