import React from 'react';
import { Link } from 'react-router-dom'



const Commit = ({data}) => {
  return (
    <p>
      <a href={data.url}>{data.short_oid}</a>
      &nbsp;|&nbsp;
      {data.message_head}
      &nbsp;|&nbsp;
      <span>
        <Link to={`/${data.repository.name}`}>{data.repository.name}</Link>
      </span>
    </p>
  )

}


export default Commit