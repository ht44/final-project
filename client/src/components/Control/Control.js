import React from 'react';
import './Control.css'

function Control(props) {
  return(
    <button className="Control" onClick={() => props.onClick(props.level, props.year, props.handler)}>
      {props.year}
    </button>
  )
}

export default Control;
