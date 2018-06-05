import React from 'react'
import { Urls } from 'utils'
import Commit from './Commit'


class CommitList extends React.Component {
  constructor(...args) {
    super(...args)
    this.state = {
      commits: [],
      isLoading: false
    }
  }

  componentDidMount() {
    this.setState({ isLoading: true })
    const url = Urls['commit-list']()
    const options = { credentials: 'same-origin' }

    fetch(url, options)
      .then(response => (response.json()))
      .then(data => {
        this.setState({
          commits: data,
          isLoading: false
        })
      })
  }

  render() {
    const { isLoading, commits } = this.state

    if (isLoading) {
      return <p>Loading...</p>
    }
    return (
      <div>
        {commits.map(data => <Commit key={data.oid} data={data} />)}
      </div>
    )
  }
}

export default CommitList