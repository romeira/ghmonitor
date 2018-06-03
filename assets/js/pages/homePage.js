import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { debug } from 'util';


const Commit = (props) => {
  const { data } = props
  return <p>{data.message_head}</p>
}


class Commits extends Component {
  constructor() {
    super()
    this.state = {
      commits: [],
      isLoading: true
    }
  }

  componentDidMount() {
    this.setState({ isLoading: true })
    const url = window.Urls['commit-list']()
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
    console.log(this.state.commits)
    return (
    <div>
    {this.state.commits.map(data => <Commit key={data.oid} data={data} />)}
    </div>
    )
  }
}

const App = () => (
  <div>
    <h1>Github Monitor</h1>
    <Commits />
  </div>
);

ReactDOM.render(<App></App>, document.getElementById('react-app'));
