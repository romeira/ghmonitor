import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import { fetchCommitsIfNeeded,
         invalidateRepository,
} from '../actions'
import { CommitList } from '../components'


class Repo extends Component {
  constructor(...args){
    super(...args)
    this.handleRefreshClick = this.handleRefreshClick.bind(this)
  }

  componentDidMount() {
    const { dispatch } = this.props
    const { repository } = this.props.match.params

    dispatch(fetchCommitsIfNeeded(repository))
  }

  handleRefreshClick(e){
    e.preventDefault()

    const { dispatch } = this.props
    const { repository } = this.props.match.params

    dispatch(invalidateRepository(repository))
    dispatch(fetchCommitsIfNeeded(repository))
  }

  render() {
    const { repository } = this.props.match.params
    const data = this.props.commitsByRepository[repository]
    if (!data) {
      return <div></div>
    }
    const { items: commits, isFetching, lastUpdated } = data

    const isEmpty = commits.length === 0
    return (
      <div>
        <h1>{repository}</h1>
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

Repo.propTypes = {
  repository: PropTypes.string,
  commitsByRepository : PropTypes.object.isRequired,
  dispatch: PropTypes.func.isRequired
}

const mapStateToProps = state => {
  const { repository, commitsByRepository } = state
  return { repository, commitsByRepository }
}

export default connect(mapStateToProps)(Repo)
