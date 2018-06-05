import React from 'react';


const Commit = ({data}) => {
  return <p><a href={data.url}>{data.short_oid}</a> {data.message_head}</p>
}

export default Commit