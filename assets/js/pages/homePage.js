import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { selectRepository, fetchCommitsIfNeeded, invalidateRepository } from '../actions'
import { CommitList, AddRepository } from '../components'


class App extends Component {
  constructor(...args){
    super(...args)

    this.handleChange = this.handleChange.bind(this)
    this.handleRefreshClick = this.handleRefreshClick.bind(this)
  }

  componentDidMount() {
    const { dispatch, selectedRepository } = this.props
    dispatch(fetchCommitsIfNeeded(selectedRepository))
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.selectedRepository !== this.props.selectedRepository) {
      const { dispatch, selectedRepository } = nextProps
      dispatch(fetchCommitsIfNeeded(selectedRepository))
    }
  }

  handleChange(nextRepository) {
    this.props.dispatch(selectRepository(nextRepository))
  }

  handleRefreshClick(e){
    e.preventDefault()

    const { dispatch, selectedRepository } = this.props
    dispatch(invalidateRepository(selectedRepository))
    dispatch(fetchCommitsIfNeeded(selectedRepository))
  }

  render() {
    const { commits, isFetching, lastUpdated } = this.props
    const isEmpty = commits.length === 0
    return (
      <div>
        <AddRepository onSubmit={this.handleChange} />
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
  selectedRepository: PropTypes.string.isRequired,
  commits: PropTypes.array.isRequired,
  isFetching: PropTypes.bool.isRequired,
  lastUpdated: PropTypes.number,
  dispatch: PropTypes.func.isRequired
}

const mapStateToProps = state => {
  const { selectedRepository, commitsByRepository } = state
  const {
    isFetching,
    lastUpdated,
    items: commits
  } = commitsByRepository[selectedRepository] || {
    isFetching: true,
    items: []
  }

  return {
    selectedRepository,
    commits,
    isFetching,
    lastUpdated
  }
}

export default connect(mapStateToProps)(App)
