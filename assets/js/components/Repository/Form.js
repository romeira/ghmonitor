import React, { Component } from 'react'
import { Urls } from 'utils'


class RepositoryForm extends Component {

  constructor(...args){
    super(...args)
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  handleSubmit(event) {
    event.preventDefault()
    const { value } = this.input

    const url = Urls['repository-list']()
    const options = {
      credentials: 'same-origin',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name: value })
    }

    fetch(url, options)
      .then(response =>{
        debugger
      })
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <label>Repository:
          <input ref={node => this.input = node} type="text" />
          <button type="submit">Submit</button>
        </label>
      </form>

    )

  }

}
export default RepositoryForm