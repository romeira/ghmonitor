import React from 'react';


const CommitItem = ({data}) => {
  return <p><a href={data.url}>{data.short_oid}</a> {data.message_head}</p>
}

export default CommitItem;