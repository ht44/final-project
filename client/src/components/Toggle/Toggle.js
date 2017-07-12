import React from 'react';
import './Toggle.css'

function Toggle(props) {
  return(
    <button className="Control" onClick={() => props.onClick(props.level)}>
      {props.level}
    </button>
  )
}

export default Toggle;
