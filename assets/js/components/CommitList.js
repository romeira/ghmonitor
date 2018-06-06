import React from 'react'
import Commit from './Commit'


const CommitList = ({commits}) => (
      <div>
        {commits.map(data => <Commit key={data.oid} data={data} />)}
      </div>
)

export default CommitList