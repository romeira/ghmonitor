import React, { Component } from 'react';
import { Urls } from 'utils'
import CommitItem from './Item'


class CommitList extends Component {
  constructor() {
    super()
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
      .then(result => (result.json()))
      .then(data => {
        this.setState({
          commits: data,
          isLoading: false
        })
      })
  }

  render() {
    if (this.state.isLoading) {
      return <p>Loading...</p>
    }
    console.log(Urls)
    return (
      <div>
        {this.state.commits.map(data => <CommitItem key={data.oid} data={data} />)}
      </div>
    )
  }
}

export default CommitList;