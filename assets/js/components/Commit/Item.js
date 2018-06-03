import React from 'react';


const CommitItem = (props) => {
  const { data } = props
  return <p>{data.message_head}</p>
}

export default CommitItem;