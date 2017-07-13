import React, { Component } from 'react';
import './Input.css'
function Input(props) {
  const legend = props.legend;
  return (
    <input className="Input" type="number" min="0" max="10" step="0.01" placeholder={legend} name={props.name} onChange={props.handleChange}/>
  );
}
export default Input;
