import React, { Component } from 'react'
import PropTypes from 'prop-types'


const AddRepository = ({ onSubmit }) => {
  let input = null

  return (
    <form onSubmit={e => {e.preventDefault(); onSubmit(input.value)}}>
      <label>Repository:
      <input ref={node => input = node} type="text" />
        <button type="submit">Submit</button>
      </label>
    </form>
  )
}

AddRepository.propTypes = {
  onSubmit: PropTypes.func.isRequired
}

export default AddRepository